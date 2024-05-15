import os

data_path = '/data/processed/kaggle'


def test_classes():
    """
    Assert that the dataset has all the classes.
    """
    true_classes = {
        'cardboard',
        'glass',
        'metal',
        'paper',
        'plastic',
        'trash'
    }
    for split_path in os.listdir(data_path):
        classes = set(os.listdir(os.path.join(data_path, split_path)))
        assert classes == true_classes


def test_splits():
    """
    Assert that the train-val-test splits are correct.
    """
    # Calculate images for all splits for all class names.
    counts = {}
    for split_path in os.listdir(data_path):
        counts[split_path] = {}
        for class_name in os.listdir(os.path.join(data_path, split_path)):
            counts[split_path][class_name] = os.listdir(
                os.path.join(data_path, split_path, class_name))

    # Assert 0.8-0.1-0.1 splits
    for split in ['val', 'test']:
        for class_name in counts[split]:
            train_files = len(list(os.listdir(os.path.join(
                data_path, 'train', class_name))))
            split_files = len(list(os.listdir(os.path.join(
                data_path, split, class_name))))
            all_files = train_files + 2 * split_files
            print(train_files, split_files)
            assert ((0.1 * all_files) - 5)\
                < split_files \
                < ((0.1 * all_files) + 5)
