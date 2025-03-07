class OpTypes(object):
    UNARY = "unary"
    BINARY = "binary"
    OTHER = "other"


class NodeTypes(object):
    INPUT = "input"
    MIDDLE = "middle"
    OUTPUT = "output"


class Operators(object):
    # Arithmetic
    LINEAR = "linear"
    ADDITION = "addition"
    SUBTRACTION = "subtraction"
    MULTIPLICATION = "multiplication"
    DIVISION = "division"
    POSITIVE = "positive"
    NEGATION = "negation"
    EXPONENTIAL = "exponential"
    NATURAL_LOG = "natural_log"
    POWER = "power"
    SQUARE = "square"
    CUBE = "cube"
    SQUARE_ROOT = "square_root"
    CUBE_ROOT = "cube_root"
    ABSOLUTE = "absolute"

    # Matrix
    MATRIX_MULTIPLICATION = "matrix_multiplication"
    MULTIPLY = "multiply"  # Elementwise multiplication
    DOT = "dot"
    TRANSPOSE = "transpose"
    MATRIX_SUM = "matrix_sum"
    SORT = "sort"
    SPLIT = "split"
    RESHAPE = "reshape"
    CONCATENATE = "concatenate"
    MIN = "min"
    MAX = "max"
    UNIQUE = "unique"
    ARGMAX = "argmax"
    ARGMIN = "argmin"
    EXPAND_DIMS = "expand_dims"
    INVERSE = "inv"
    GATHER = "gather"
    REVERSE = "reverse"
    STACK = "stack"
    TILE = "tile"
    SLICE = "slice"
    FIND_INDICES = "find_indices"
    SHAPE = "shape"
    PAD = "pad"
    ARANGE = "arange"
    REPEAT = "repeat"
    INDEX = "index"

    # Comparison Operators
    GREATER = "greater"
    GREATER_EQUAL = "greater_equal"
    LESS = "less"
    LESS_EQUAL = "less_equal"
    EQUAL = "equal"
    NOT_EQUAL = "not_equal"

    # Logical
    LOGICAL_AND = "logical_and"
    LOGICAL_OR = "logical_or"
    LOGICAL_NOT = "logical_not"
    LOGICAL_XOR = "logical_xor"

    # Statistical
    MEAN = "mean"
    AVERAGE = "average"
    MODE = "mode"
    VARIANCE = "variance"
    MEDIAN = "median"
    STANDARD_DEVIATION = "standard_deviation"
    PERCENTILE = "percentile"
    RANDOM = "random"

    BINCOUNT = "bincount"
    WHERE = "where"
    SIGN = "sign"
    FOREACH = "foreach"
    CLIP = "clip"
    RANDOM_UNIFORM = "random_uniform"
    PROD = "prod"
    FLATTEN = "flatten"
    RAVEL = "ravel"
    JOIN_TO_LIST = "join_to_list"
    COMBINE_TO_LIST = "combine_to_list"
    ZEROS = "zeros"
    RAVINT = "ravint"
    CNN_INDEX = "cnn_index"
    CNN_INDEX_2 = "cnn_index_2"
    CNN_ADD_AT = "cnn_add_at"
    SIZE = "size"
    SQUEEZE = "squeeze"
    LINEAR_REGRESSION = "linear_regression"
    LOGISTIC_REGRESSION = "logistic_regression"
    KNN_CLASSIFIER = "knn_classifier"
    KNN_REGRESSOR = "knn_regressor"
    NAIVE_BAYES = "naive_bayes"
    KMEANS = "kmeans"
    SVM_SVC = "svm_svc"
    SVM_SVR = "svm_svr"
    DECISION_TREE_CLASSIFIER = "decision_tree_classifier"
    DECISION_TREE_REGRESSOR = "decision_tree_regressor"
    RANDOM_FOREST_CLASSIFIER = "random_forest_classifier"
    RANDOM_FOREST_REGRESSOR = "random_forest_regressor"

    FORWARD_PASS_DENSE = "forward_pass_dense"
    BACKWARD_PASS_DENSE = "backward_pass_dense"
    FORWARD_PASS_BATCHNORM = "forward_pass_batchnorm"
    BACKWARD_PASS_BATCHNORM = "backward_pass_batchnorm"
    FORWARD_PASS_DROPOUT = "forward_pass_dropout"
    BACKWARD_PASS_DROPOUT = "backward_pass_dropout"
    FORWARD_PASS_ACTIVATION = "forward_pass_activation"
    BACKWARD_PASS_ACTIVATION = "backward_pass_activation"
    FORWARD_PASS_CONV2D = "forward_pass_conv2d"
    BACKWARD_PASS_CONV2D = "backward_pass_conv2d"
    FORWARD_PASS_FLATTEN = "forward_pass_flatten"
    BACKWARD_PASS_FLATTEN = "backward_pass_flatten"
    FORWARD_PASS_MAXPOOL2D = "forward_pass_maxpool2d"
    BACKWARD_PASS_MAXPOOL2D = "backward_pass_maxpool2d"

    SQUARE_LOSS = "square_loss"
    SQUARE_LOSS_GRADIENT = "square_loss_gradient"
    CROSS_ENTROPY_LOSS = "cross_entropy_loss"
    CROSS_ENTROPY_GRADIENT = "cross_entropy_gradient"
    CROSS_ENTROPY_ACCURACY = "cross_entropy_accuracy"


    # Data Preprocessing
    ONE_HOT_ENCODING = "one_hot_encoding"

    SET_VALUE = "set_value"
    GET_LAYER_RESULTS="get_layer_result"
    
    FEDERATED_MEAN = "federated_mean"
    FEDERATED_VARIANCE = "federated_variance"
    FEDERATED_STANDARD_DEVIATION = "federated_standard_deviation"


class TFJSOperators(object):
    SIGMOID = "sigmoid"
    SIN = "sin"
    SINH = "sinh"
    SOFTPLUS = "softplus"


functions = {'lin': Operators.LINEAR,
             'add': Operators.ADDITION,
             'sub': Operators.SUBTRACTION,
             'mul': Operators.MULTIPLICATION,
             'div': Operators.DIVISION,
             'pos': Operators.POSITIVE,
             'neg': Operators.NEGATION,
             'exp': Operators.EXPONENTIAL,
             'natlog': Operators.NATURAL_LOG,
             'pow': Operators.POWER,
             'square': Operators.SQUARE,
             'cube': Operators.CUBE,
             'square_root': Operators.SQUARE_ROOT,
             'cube_root': Operators.CUBE_ROOT,
             'abs': Operators.ABSOLUTE,
             'matmul': Operators.MATRIX_MULTIPLICATION,
             'multiply': Operators.MULTIPLY,
             'dot': Operators.DOT,
             'transpose': Operators.TRANSPOSE,
             'sum': Operators.MATRIX_SUM,
             'sort': Operators.SORT,
             'split': Operators.SPLIT,
             'reshape': Operators.RESHAPE,
             'concat': Operators.CONCATENATE,
             'min': Operators.MIN,
             'max': Operators.MAX,
             'unique': Operators.UNIQUE,
             'argmax': Operators.ARGMAX,
             'argmin': Operators.ARGMIN,
             'expand_dims': Operators.EXPAND_DIMS,
             'inv': Operators.INVERSE,
             'gather': Operators.GATHER,
             'reverse': Operators.REVERSE,
             'stack': Operators.STACK,
             'tile': Operators.TILE,
             'slice': Operators.SLICE,
             'find_indices': Operators.FIND_INDICES,
             'shape': Operators.SHAPE,
             'greater': Operators.GREATER,
             'greater_equal': Operators.GREATER_EQUAL,
             'less': Operators.LESS,
             'less_equal': Operators.LESS_EQUAL,
             'equal': Operators.EQUAL,
             'not_equal': Operators.NOT_EQUAL,
             'logical_and': Operators.LOGICAL_AND,
             'logical_or': Operators.LOGICAL_OR,
             'logical_not': Operators.LOGICAL_NOT,
             'logical_xor': Operators.LOGICAL_XOR,
             'mean': Operators.MEAN,
             'average': Operators.AVERAGE,
             'mode': Operators.MODE,
             'variance': Operators.VARIANCE,
             'median': Operators.MEDIAN,
             'std': Operators.STANDARD_DEVIATION,
             'percentile': Operators.PERCENTILE,
             'random': Operators.RANDOM,
             'bincount': Operators.BINCOUNT,
             'where': Operators.WHERE,
             'sign': Operators.SIGN,
             'foreach': Operators.FOREACH,
             'one_hot_encoding': Operators.ONE_HOT_ENCODING,
             'set_value': Operators.SET_VALUE,
             'clip': Operators.CLIP,
             'random_uniform': Operators.RANDOM_UNIFORM,
             'prod': Operators.PROD,
             'flatten': Operators.FLATTEN,
             'ravel': Operators.RAVEL,
             'pad': Operators.PAD,
             'arange': Operators.ARANGE,
             'repeat':Operators.REPEAT,
             'index': Operators.INDEX,
             'join_to_list': Operators.JOIN_TO_LIST,
             'combine_to_list': Operators.COMBINE_TO_LIST,
             'zeros': Operators.ZEROS,
             'ravint': Operators.RAVINT,
             'cnn_index': Operators.CNN_INDEX,
             'cnn_index_2': Operators.CNN_INDEX_2,
             'cnn_add_at': Operators.CNN_ADD_AT,
             'size': Operators.SIZE,
             'squeeze': Operators.SQUEEZE,
             'linear_regression': Operators.LINEAR_REGRESSION,
             'logistic_regression': Operators.LOGISTIC_REGRESSION,
             'knn_classifier': Operators.KNN_CLASSIFIER,
             'knn_regressor': Operators.KNN_REGRESSOR,
             'naive_bayes': Operators.NAIVE_BAYES,
             'kmeans': Operators.KMEANS,
             'svm_svc': Operators.SVM_SVC,
             'svm_svr': Operators.SVM_SVR,
             'decision_tree_classifier': Operators.DECISION_TREE_CLASSIFIER,
             'decision_tree_regressor': Operators.DECISION_TREE_REGRESSOR,
             'random_forest_classifier': Operators.RANDOM_FOREST_CLASSIFIER,
             'random_forest_regressor': Operators.RANDOM_FOREST_REGRESSOR,
             'get_layer_result':Operators.GET_LAYER_RESULTS,

             'forward_pass_dense': Operators.FORWARD_PASS_DENSE,
             'backward_pass_dense': Operators.BACKWARD_PASS_DENSE,
             'forward_pass_batchnorm': Operators.FORWARD_PASS_BATCHNORM,
             'backward_pass_batchnorm': Operators.BACKWARD_PASS_BATCHNORM,
             'forward_pass_dropout': Operators.FORWARD_PASS_DROPOUT,
             'backward_pass_dropout': Operators.BACKWARD_PASS_DROPOUT,
             'forward_pass_activation': Operators.FORWARD_PASS_ACTIVATION,
             'backward_pass_activation': Operators.BACKWARD_PASS_ACTIVATION,
             'forward_pass_conv2d': Operators.FORWARD_PASS_CONV2D,
             'backward_pass_conv2d': Operators.BACKWARD_PASS_CONV2D,
             'forward_pass_flatten': Operators.FORWARD_PASS_FLATTEN,
             'backward_pass_flatten': Operators.BACKWARD_PASS_FLATTEN,
             'forward_pass_maxpool2d': Operators.FORWARD_PASS_MAXPOOL2D,
             'backward_pass_maxpool2d': Operators.BACKWARD_PASS_MAXPOOL2D,

             'square_loss': Operators.SQUARE_LOSS,
             'square_loss_gradient': Operators.SQUARE_LOSS_GRADIENT,
             'cross_entropy_loss': Operators.CROSS_ENTROPY_LOSS,
             'cross_entropy_gradient': Operators.CROSS_ENTROPY_GRADIENT,
             'cross_entropy_accuracy': Operators.CROSS_ENTROPY_ACCURACY,
             # Federated functions

             'federated_mean': Operators.FEDERATED_MEAN,
             'federated_variance': Operators.FEDERATED_VARIANCE,
             'federated_standard_deviation': Operators.FEDERATED_STANDARD_DEVIATION,
             
             }


class Status(object):
    PENDING = "pending"
    COMPUTED = "computed"
    FAILED = "failed"
    COMPUTING = "computing"


class OpStatus(Status):
    pass


class GraphStatus(Status):
    pass


class MappingStatus(Status):
    SENT = "sent"
    ACKNOWLEDGED = "acknowledged"
    NOT_ACKNOWLEDGED = "not_acknowledged"
    NOT_COMPUTED = "not_computed"
    REJECTED = "rejected"
