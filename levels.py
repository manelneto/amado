STARTS = {
    1: [
        ['b', 'b', 'b'],
        ['y', 'b', 'b'],
        ['b', 'b', 'b'],
    ],
    2: [
        ['b', 'b', 'r'],
        ['y', 'r', 'b'],
        ['r', 'y', 'r'],
    ],
    3: [
        ['y', 'y', 'r'],
        ['r', 'r', 'b'],
        ['b', 'y', 'y'],
    ],
    4: [
        ['y', 'b', 'y', 'r'],
        ['r', 'r', 'b', 'r'],
        ['y', 'y', 'b', 'r'],
        ['y', 'b', 'y', 'y'],
    ],
    5: [
        ['y', 'r', 'n', 'b'],
        ['b', 'b', 'b', 'r'],
        ['n', 'y', 'b', 'r'],
        ['r', 'r', 'b', 'b'],
    ],
    6: [
        ['n', 'b', 'b', 'b'],
        ['y', 'y', 'r', 'r'],
        ['n', 'y', 'n', 'b'],
        ['r', 'y', 'b', 'y'],
    ],
    7: [
        ['b', 'b', 'n', 'r', 'b'],
        ['r', 'b', 'r', 'y', 'r'],
        ['y', 'b', 'n', 'b', 'y'],
        ['y', 'y', 'y', 'y', 'y'],
        ['r', 'y', 'n', 'r', 'b'],
    ],
    8: [
        ['r', 'b', 'b', 'b', 'r'],
        ['b', 'b', 'b', 'b', 'y'],
        ['b', 'b', 'b', 'r', 'y'],
        ['r', 'r', 'b', 'b', 'r'],
        ['y', 'b', 'b', 'b', 'r'],
    ],
    9: [
        ['n', 'n', 'y', 'b', 'n', 'n'],
        ['n', 'b', 'b', 'r', 'y', 'n'],
        ['b', 'b', 'y', 'r', 'y', 'r'],
        ['r', 'r', 'b', 'b', 'r', 'b'],
        ['n', 'b', 'y', 'r', 'r', 'n'],
        ['n', 'n', 'b', 'r', 'n', 'n'],
    ],
    10: [
        ['n', 'n', 'n', 'n', 'r', 'n', 'n', 'n'],
        ['n', 'n', 'n', 'r', 'y', 'r', 'b', 'n'],
        ['n', 'n', 'b', 'b', 'b', 'n', 'y', 'n'],
        ['n', 'b', 'r', 'y', 'n', 'r', 'r', 'r'],
        ['b', 'b', 'b', 'n', 'r', 'y', 'b', 'n'],
        ['n', 'b', 'n', 'b', 'r', 'r', 'n', 'n'],
        ['n', 'n', 'b', 'r', 'r', 'n', 'n', 'n'],
        ['n', 'n', 'n', 'b', 'n', 'n', 'n', 'n'],
    ],
}


GOALS = {
    1: [
        ['b', 'b', 'r'],
        ['r', 'y', 'b'],
        ['y', 'r', 'b'],
    ],
    2: [
        ['y', 'y', 'y'],
        ['r', 'r', 'b'],
        ['r', 'b', 'b'],
    ],
    3: [
        ['r', 'r', 'y'],
        ['b', 'r', 'r'],
        ['y', 'y', 'b'],
    ],
    4: [
        ['r', 'r', 'b', 'r'],
        ['y', 'r', 'r', 'y'],
        ['b', 'y', 'b', 'b'],
        ['b', 'b', 'b', 'y'],
    ],
    5: [
        ['r', 'y', 'n', 'r'],
        ['y', 'y', 'r', 'y'],
        ['n', 'b', 'b', 'b'],
        ['r', 'y', 'b', 'b'],
    ],
    6: [
        ['n', 'y', 'b', 'r'],
        ['y', 'y', 'r', 'y'],
        ['n', 'b', 'n', 'b'],
        ['r', 'y', 'b', 'b'],
    ],
    7: [
        ['y', 'r', 'n', 'r', 'b'],
        ['r', 'b', 'b', 'y', 'y'],
        ['y', 'b', 'n', 'b', 'y'],
        ['r', 'y', 'y', 'b', 'r'],
        ['y', 'y', 'n', 'r', 'y'],
    ],
    8: [
        ['b', 'b', 'b', 'y', 'y'],
        ['b', 'b', 'r', 'r', 'r'],
        ['b', 'y', 'y', 'y', 'r'],
        ['r', 'r', 'r', 'y', 'r'],
        ['b', 'b', 'r', 'y', 'b'],
    ],
    9: [
        ['n', 'n', 'r', 'r', 'n', 'n'],
        ['n', 'y', 'b', 'y', 'y', 'n'],
        ['b', 'r', 'b', 'r', 'r', 'b'],
        ['r', 'r', 'y', 'b', 'y', 'y'],
        ['n', 'b', 'y', 'y', 'b', 'n'],
        ['n', 'n', 'b', 'r', 'n', 'n'],
    ],
    10: [
        ['n', 'n', 'n', 'n', 'y', 'n', 'n', 'n'],
        ['n', 'n', 'n', 'r', 'b', 'y', 'b', 'n'],
        ['n', 'n', 'y', 'b', 'r', 'n', 'y', 'n'],
        ['n', 'r', 'b', 'y', 'n', 'r', 'b', 'y'],
        ['y', 'b', 'r', 'n', 'y', 'b', 'r', 'n'],
        ['n', 'y', 'n', 'r', 'b', 'y', 'n', 'n'],
        ['n', 'n', 'y', 'b', 'r', 'n', 'n', 'n'],
        ['n', 'n', 'n', 'y', 'n', 'n', 'n', 'n'],
    ],
}
