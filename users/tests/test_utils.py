from unittest.mock import patch
from users.utils import write_to_csv


def test_write_to_csv():
    with patch('users.utils.open', create=False) as test_open:
        write_to_csv('test.csv', ('id', 'email'), ('1', 'test@test.pl'))
        test_open.assert_called()
