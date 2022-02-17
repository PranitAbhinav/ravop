import ast
import json
import sys
import time
from functools import wraps

import numpy as np

from ..globals import globals as g
from ..strings import OpTypes, NodeTypes, functions, OpStatus
from ..utils import make_request, convert_to_ndarray


def t(value, dtype="ndarray", **kwargs):
    """
    To create scalars, tensors and other data types
    """
    if dtype == "ndarray":
        if isinstance(value, int):
            return Scalar(value, **kwargs)
        elif isinstance(value, float):
            return Scalar(value, **kwargs)
        else:
            return Tensor(value, **kwargs)
    elif dtype == "file":
        return File(value=value, dtype=dtype, **kwargs)


def create_op(operator=None, *args, **params):
    return __create_math_op(operator=operator, *args, **params)


def epsilon():
    return Scalar(1e-07)


def one():
    return Scalar(1)


def minus_one():
    return Scalar(-1)


def inf():
    return Scalar(np.inf)


def pi():
    return Scalar(np.pi)


def __create_math_op(*args, **kwargs):
    params = dict()
    for key, value in kwargs.items():
        if key in ["node_type", "op_type", "status", "name", "operator"]:
            continue
        if (
                isinstance(value, Op)
                or isinstance(value, Data)
                or isinstance(value, Scalar)
                or isinstance(value, Tensor)
        ):
            params[key] = value.id
        elif type(value).__name__ in ["int", "float"]:
            params[key] = Scalar(value).id
        elif isinstance(value, list) or isinstance(value, tuple):
            params[key] = Tensor(value).id
        elif type(value).__name__ == "str":
            params[key] = value
        elif isinstance(value, bool):
            params[key] = value

    if len(args) == 0:
        op_ids = None
        op_type = None
        node_type = None
    else:
        op_ids = []
        for op in args:
            op_ids.append(op.id)

        if len(op_ids) == 1:
            op_type = OpTypes.UNARY
        elif len(op_ids) == 2:
            op_type = OpTypes.BINARY
        else:
            op_type = None

        node_type = NodeTypes.MIDDLE

    if op_ids is not None:
        op_ids = json.dumps(op_ids)
    node_type = kwargs.get("node_type", node_type)
    op_type = kwargs.get("op_type", op_type)
    status = kwargs.get("status", OpStatus.PENDING)
    operator = kwargs.get("operator", None)
    complexity = kwargs.get("complexity", None)

    op = make_request("op/create/", "post", {
        "name": kwargs.get("name", None),
        "graph_id": g.graph_id,
        "subgraph_id": g.sub_graph_id,
        "node_type": node_type,
        "inputs": op_ids,
        "outputs": None,
        "op_type": op_type,
        "operator": operator,
        "status": status,
        "complexity": complexity,
        "params": json.dumps(params),
    })

    op = op.json()
    op = Op(id=op["id"])
    if g.eager_mode:
        op.wait_till_computed()
    return op


class ParentClass(object):
    def __init__(self, id=None, **kwargs):
        self._error = None
        self._status_code = None

        if id is not None:
            self.__get(endpoint=self.get_endpoint)
        else:
            self.__create(self.create_endpoint, **kwargs)

    def fetch_update(self):
        self.__get(self.get_endpoint)

    def __get(self, endpoint):
        # print('ENDPOINT: ',endpoint)
        res = make_request(endpoint, "get")
        # print("Response:GET:", res.json())
        status_code = res.status_code
        res = res.json()
        if status_code == 200:
            for k, v in res.items():
                self.__dict__[k] = v
            self._status_code = 200
        else:
            self._error = res['message']
            self._status_code = status_code

    def __create(self, endpoint, **kwargs):
        res = make_request(endpoint, "post", payload={**kwargs})
        # print("Response:POST:", res.text, kwargs)
        status_code = res.status_code
        res = res.json()
        if status_code == 200:
            # Set class attributes
            for k, v in res.items():
                self.__dict__[k] = v
            self._status_code = 200
        else:
            self._error = res['message']
            self._status_code = status_code

    @property
    def error(self):
        if hasattr(self, "_error"):
            return self._error
        return None

    @property
    def status_code(self):
        if hasattr(self, "_status_code"):
            return self._status_code
        return None

    def valid(self):
        if self.status_code == 200:
            return True
        else:
            return False


class Op(ParentClass):
    def __init__(self, id=None, **kwargs):
        self.get_endpoint = f"op/get/?id={id}"
        self.create_endpoint = f"op/create/"

        if id is not None:
            super().__init__(id=id)
        else:

            inputs = kwargs.get("inputs", None)
            outputs = kwargs.get("outputs", None)
            operator = kwargs.get("operator", None)

            if (inputs is not None or outputs is not None) and operator is not None:
                info = self.extract_info(**kwargs)
                info['graph_id'] = g.graph_id
                info['subgraph_id'] = g.sub_graph_id
                info['params'] = json.dumps(kwargs)
                info["name"] = kwargs.get("name", None)

                super().__init__(id, **info)

    def wait_till_computed(self):
        print('Waiting for Op id: ', self.id)
        while self.get_status() != 'computed':
            time.sleep(0.1)
        sys.stdout.write("\033[F")  # back to previous line
        sys.stdout.write("\033[K")  # clear line

    def get_status(self):
        return make_request(f"op/status/?id={self.id}", "get").json()['op_status']

    def extract_info(self, **kwargs):
        inputs = kwargs.get("inputs", None)
        outputs = kwargs.get("outputs", None)
        operator = kwargs.get("operator", None)

        # Figure out node type
        if inputs is None and outputs is not None:
            node_type = NodeTypes.INPUT
        elif inputs is not None and outputs is None:
            node_type = NodeTypes.MIDDLE
        else:
            raise Exception("Invalid node type")

        if inputs is not None:
            if len(inputs) == 1:
                op_type = OpTypes.UNARY
            elif len(inputs) == 2:
                op_type = OpTypes.BINARY
            else:
                raise Exception("Invalid number of inputs")
        else:
            op_type = OpTypes.OTHER

        if outputs is None:
            status = OpStatus.PENDING
        else:
            status = OpStatus.COMPUTED

        inputs = json.dumps(inputs)
        outputs = json.dumps(outputs)

        return {
            "node_type": node_type,
            "op_type": op_type,
            "status": status,
            "inputs": inputs,
            "outputs": outputs,
            "operator": operator
        }

    def get_output(self):
        return self.get_data().get_value()

    def get_dtype(self):
        return self.get_data().get_dtype()

    def get_shape(self):
        return self.get_data().get_shape()

    def get_data(self):
        if self.outputs is None or self.outputs == "null":
            return None

        data_id = json.loads(self.outputs)[0]
        data = Data(id=data_id)
        return data

    def __str__(self):
        return (
            "Op:\nId:{}\nName:{}\nType:{}\nOperator:{}\n\nStatus:{}\n".format(
                self.id,
                self.name,
                self.op_type,
                self.operator,
                self.status,
            )
        )

    def __call__(self, *args, **kwargs):
        self.wait_till_computed()
        self.fetch_update()
        temp = make_request(f"global/subgraph/update/id/?graph_id={g.graph_id}", "get").json()['global_subgraph_id']
        g.sub_graph_id = temp + 1
        return self.get_output()

    def __add__(self, other):
        return add(self, other)

    def __sub__(self, other):
        return sub(self, other)

    def __mul__(self, other):
        return mul(self, other)

    def __pos__(self):
        return pos(self)

    def __neg__(self):
        return neg(self)

    def __abs__(self):
        return abs(self)

    def __invert__(self):
        return inv(self)

    def __lt__(self, other):
        return less(self, other)

    def __le__(self, other):
        return less_equal(self, other)

    def __eq__(self, other):
        return equal(self, other)

    def __ne__(self, other):
        return not_equal(self, other)

    def __ge__(self, other):
        return greater_equal(self, other)

    def __getitem__(self, item):
        if type(item).__name__ == "slice":
            return self.slice(begin=item.start, size=item.stop - item.start)
        elif type(item).__name__ == "int":
            return self.gather(Scalar(item))
        elif type(item).__name__ == "tuple":
            var = self
            for i in item:
                var = var.gather(Scalar(i))
            return var


def add_method(cls):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        setattr(cls, func.__name__, wrapper)
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func  # returning func means func can still be used normally

    return decorator


for key, value in functions.items():
    exec(
        """@add_method(Op)\ndef {}(*args, **kwargs):\n    return __create_math_op(*args, operator="{}", **kwargs)""".format(
            key, key
        )
    )


class Scalar(Op):
    def __init__(self, value=None, id=None, data=None, **kwargs):
        if id is not None:
            # Get
            super().__init__(id=id)

        elif data is not None:
            if data.valid():

                # Create scalar
                super().__init__(
                    operator="lin", inputs=None, outputs=[data.id], **kwargs
                )
            else:
                self.__dict__['_status_code'] = 400
                self.__dict__['_error'] = "Invalid data"

        elif value is not None:
            # Create data and then op

            data = Data(value=value)
            if data.valid():
                super().__init__(
                    operator="lin", inputs=None, outputs=[data.id], **kwargs
                )
            else:
                self.__dict__['_status_code'] = 400
                self.__dict__['_error'] = "Invalid data"

    def __str__(self):
        return "Scalar Op:\nId:{}\nOutput:{}\nStatus:{}\nDtype:{}\n".format(
            self.id, self.get_output(), self.status, self.get_dtype
        )

    def __float__(self):
        return float(self.get_output())


class Tensor(Op):
    """
    It supports:
    1. list
    2. ndarray
    3. string(list)
    """

    def __init__(self, value=None, id=None, data=None, **kwargs):
        if id is not None:
            # Get
            super().__init__(id=id)

        elif data is not None:
            if data.valid():
                # Create scalar
                super().__init__(
                    operator="lin", inputs=None, outputs=[data.id], **kwargs
                )
            else:
                self.__dict__['_status_code'] = 400
                self.__dict__['_error'] = "Invalid data"

        elif value is not None:
            # Create data and then op
            data = Data(value=value)
            if data.valid():
                super().__init__(
                    operator="lin", inputs=None, outputs=[data.id], **kwargs
                )
            else:
                self.__dict__['_status_code'] = 400
                self.__dict__['_error'] = "Invalid data"

    def __str__(self):
        return "Tensor Op:\nId:{}\nOutput:{}\nStatus:{}\nDtype:{}".format(
            self.id, self.get_output(), self.status, self.get_dtype
        )


class File(Op):
    def __init__(self, value, **kwargs):
        data = Data(value=value, dtype="file")
        super().__init__(
            operator="lin", inputs=None, outputs=[data.id], **kwargs
        )

    @property
    def dtype(self):
        return "file"

    @property
    def shape(self):
        return None

    def __str__(self):
        return "File Op:\nId:{}\nOutput:{}\nStatus:{}\nDtype:{}\n".format(
            self.id, self.get_output(), self.status, self.dtype
        )

    def __call__(self, *args, **kwargs):
        return self.get_output()


class Data(ParentClass):
    def __init__(self, value=None, id=None, **kwargs):
        self.get_endpoint = f"data/get/?id={id}"
        self.create_endpoint = f"data/create/"

        # value = kwargs.get("value", None)
        if value is not None and isinstance(value, np.ndarray):
            value = value.tolist()
            kwargs['value'] = value
        else:
            kwargs['value'] = value

        super().__init__(id, **kwargs)

    def __call__(self, *args, **kwargs):
        self.fetch_update()
        return self.get_value()

    def get_value(self):
        if hasattr(self, 'value'):
            return convert_to_ndarray(self.value)
        else:
            return None

    def get_dtype(self):
        if hasattr(self, "dtype"):
            return self.dtype
        else:
            return None

    def get_shape(self):
        if hasattr(self, 'value'):
            if self.value is not None:
                return self.value.shape
        return None


class Graph(ParentClass):
    """A class to represent a graph object"""

    def __init__(self, id=None, **kwargs):

        self.get_graph_id_endpoint = f"graph/get/graph_id"
        res = make_request(self.get_graph_id_endpoint, "get")
        g.graph_id = res.json()["graph_id"]
        if id is None:
            id = g.graph_id + 1
            self.my_id = id - 1
            g.sub_graph_id = 1
        else:
            self.my_id = id

        self.get_endpoint = f"graph/get/?id={id}"
        self.create_endpoint = f"graph/create/"

        if id is not None and id <= g.graph_id:
            super().__init__(id=id)
        else:
            super().__init__(**kwargs)

    # def add(self, op):
    #     """Add an op to the graph"""
    #     op.add_to_graph(self.id)

    @property
    def progress(self):
        get_progress_endpoint = f"graph/op/get/progress/?id={self.my_id}"
        res = make_request(get_progress_endpoint, "get")
        return res.json()['progress']

    def end(self):
        """End the graph"""
        end_endpoint = f"graph/end/?id={self.my_id}"
        res = make_request(end_endpoint, "get")
        print('\n')
        print(res.json()['message'])
        return res.json()['message']

    def get_op_stats(self):
        """Get stats of all ops"""
        get_op_stats_endpoint = f"graph/op/get/stats/?id={self.my_id}"
        res = make_request(get_op_stats_endpoint, "get")
        return res.json()

    # def clean(self):
    #     ravdb.delete_graph_ops(self._graph_db.id)

    @property
    def ops(self):
        """Get all ops associated with a graph"""
        get_graph_ops_endpoint = f"graph/op/get/?id={self.my_id}"
        res = make_request(get_graph_ops_endpoint, "get")
        res = res.json()
        return res

    def get_ops_by_name(self, op_name, graph_id=None):
        get_ops_by_name_endpoint = f"graph/op/name/get/?op_name={op_name}&id={graph_id}"
        res = make_request(get_ops_by_name_endpoint, "get")
        res = res.json()
        return res

    def get_subgraphs(self):
        get_op_dependency_endpoint = f"graph/op_dependency/get/?id={self.my_id}"
        res = make_request(get_op_dependency_endpoint, "get")
        res = res.json()
        op_dependency = res['op_dependency']
        print('\n\n OP_Dependency: ', op_dependency)
        min_op_id = res['min_op_id']
        cc = self.find_subgraphs(op_dependency, min_op_id)
        return cc

    def find_subgraphs(self, g_nodes, min_op_id):
        update_subgraph_op_mapping_endpoint = f"subgraph/op/mappings/"
        current_graph = {}
        for k in g_nodes:
            if g_nodes[k] != 'null':
                g_nodes[k] = ast.literal_eval(g_nodes[k])
                g_nodes[k] = [i - min_op_id - 1 for i in g_nodes[k]]
            current_graph[int(k) - 1] = g_nodes[k]
        m = 0
        for k in current_graph:
            m += 1
        sg = SubGraph(m)

        for k in current_graph:
            if current_graph[k] != 'null':
                for i in current_graph[k]:
                    sg.addEdge(int(k), int(i))

        cc = sg.connectedComponents()
        subgraphs_list = []
        for i in cc:
            subgraphs_list.append([j + min_op_id + 1 for j in i])

        max_subgraph_id = len(subgraphs_list)
        subgraphs = {}

        for i in range(max_subgraph_id):
            subgraphs[i + 1] = subgraphs_list[i]

        res = make_request(update_subgraph_op_mapping_endpoint, "post", payload=subgraphs)

        return subgraphs

    def __str__(self):
        return "Graph:\nId:{}\nStatus:{}\n".format(self.id, self.status)


class SubGraph:
    def __init__(self, V):
        self.V = V
        self.adj = [[] for i in range(V)]

    def DFSUtil(self, temp, v, visited):
        visited[v] = True
        temp.append(v)
        for i in self.adj[v]:
            if visited[i] == False:
                temp = self.DFSUtil(temp, i, visited)
        return temp

    def addEdge(self, v, w):
        self.adj[v].append(w)
        self.adj[w].append(v)

    def connectedComponents(self):
        visited = []
        cc = []
        for i in range(self.V):
            visited.append(False)
        for v in range(self.V):
            if visited[v] == False:
                temp = []
                cc.append(self.DFSUtil(temp, v, visited))
        return cc
