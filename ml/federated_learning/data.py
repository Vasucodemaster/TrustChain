import torch


def create_institution_data(institution_id):
    if institution_id == 1:
        data = [
            [90, 85, 88, 92, 80, 95],
            [75, 70, 78, 80, 72, 76],
            [95, 92, 94, 96, 90, 98],
            [65, 60, 70, 68, 64, 66],
            [85, 88, 82, 90, 86, 89],
        ]

    elif institution_id == 2:
        data = [
            [80, 82, 85, 78, 84, 81],
            [92, 90, 91, 94, 89, 93],
            [70, 68, 72, 75, 69, 71],
            [88, 86, 90, 87, 85, 91],
            [76, 79, 74, 80, 77, 78],
        ]

    else:
        data = [
            [95, 94, 96, 93, 92, 97],
            [82, 80, 84, 86, 81, 85],
            [68, 72, 65, 70, 67, 69],
            [90, 88, 92, 91, 89, 94],
            [78, 75, 80, 77, 79, 76],
        ]

    x = torch.tensor(data, dtype=torch.float32)

    # Target reputation score
    y = torch.mean(x, dim=1, keepdim=True)

    return x, y
