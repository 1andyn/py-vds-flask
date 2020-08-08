import unittest
import driver
import event


class TestApplicationFunctions(unittest.TestCase):

    def test_event_creation(self):
        e = event.Event("123", "test event", "bob")
        self.assertIs("123", e.getId())
        self.assertIs("test event", e.getEvent())
        self.assertIs("bob", e.getDate())

    def test_db_insertion_deletion(self):
        connection = driver.Database()
        e = event.Event("777", "bobs birthday", "12-31-2020") # insert 777
        connection.insert_event(e, "alice") # insert under alice
        results = connection.get_events("alice") # check for alice rows
        self.assertIs(len(results), 1) # count should be one
        connection.del_one_event("alice", "111") # delete 111, shouldn't do anything
        self.assertIs(len(results), 1) # should still be one
        connection.del_one_event("alice", "777") # delete 777
        results = connection.get_events("alice")
        self.assertIs(len(results), 0) # should be 0

    def test_db_retrieval(self):
        connection = driver.Database()
        results = connection.get_events("bob")
        self.assertIs(len(results), 0) # should not have results

    def test_db_deletion(self):
        connection = driver.Database()
        e1 = event.Event("id124", "marys birthday", "12-31-2020")
        e2 = event.Event("id707", "bobs birthday", "12-31-2020")
        e3 = event.Event("id884", "keiths birthday", "12-31-2020")
        connection.insert_event(e1, "andy")
        connection.insert_event(e2, "andy")
        connection.insert_event(e3, "andy")
        connection.del_events("andy")
        results = connection.get_events("andy")
        self.assertIs(len(results), 0)


if __name__ == '__main__':
    unittest.main()
