import unittest
from flask import Flask
from WebPipeline import *
from mockobjects import *

class Unittest_GenerateModule(unittest.TestCase):
  def setUp(self):
    self.dispenser = Modules.GenerateModule()
    
  def test_add(self):
    self.dispenser.add(MockModule())
    self.assertEqual(self.dispenser.module[0].name, "test")

  def test_find_rightValue(self):
    self.dispenser.add(MockModule())
    self.assertEqual(self.dispenser.find("test"), self.dispenser.module[0])

  def test_find_wrongValue(self):
    self.dispenser.add(MockModule())
    self.assertEqual(self.dispenser.find("niet-test"), False)
 
class Unittest_Module(unittest.TestCase):
  def setUp(self):
    self.module = Modules.Module("testmodule",[MockTask()],"testdescription")
  
  def test_find(self):
    self.assertEqual(self.module.find("testtask").name,"testtask")

  def test_find_wrong_task(self):
    self.assertNotEqual(self.module.find("testtask").name,"Task not found")

class Unittest_Grader(unittest.TestCase):
  def setUp(self):
    self.module = Modules.Grader(MockInjector())
  
  def test_find(self):
    self.assertTrue(self.module.grade(["test","testtask",0],"testwoord"))

  def test_find_wrong_value(self):
    self.assertFalse(self.module.grade(["test","testtask",0],"Wrong Value"))


class Unittest_flask(unittest.TestCase):
  def setUp(self):
    Modules.injector.overrideModule(MockDispenser())
    self.app = app.test_client()
    self.app.secret_key = os.urandom(24)
    self.app.testing = True

  def test_homepage_load(self):
    result = self.app.get('/')
    self.assertEqual(result.status_code,200)

  def test_correctmodule_load(self):
    result = self.app.get('/module/test')
    self.assertEqual(result.status_code,200)

  def test_wrongmodule_load(self):
    result = self.app.get('/module/Verkeerde value')
    self.assertNotEqual(result.status_code,200)

  def test_404_load(self):
    result = self.app.get('/404')
    self.assertEqual(result.status_code,200)

  def test_404_redirects(self):
    result = self.app.get('/Verkeerde value')
    self.assertEqual(result.location,"http://localhost/404")

  def test_check_correct_value(self):
    result = self.app.get("/check/test/testtask")
    self.assertEqual(result.location,"http://localhost/assignment")

  def test_check_wrongModuleName(self):
    result = self.app.get("/check/Verkeerde value/testcab1")
    self.assertEqual(result.location,"http://localhost/404")

  def test_check_wrongTaskName(self):
    result = self.app.get("/check/test/Verkeerde value")
    self.assertEqual(result.location,"http://localhost/404")

  def test_assignment_empty_redirect(self):
    result = self.app.get("/assignment")
    self.assertEqual(result.location,"http://localhost/")

  def test_task_mock(self):
    with self.app.session_transaction() as session:
      session['currentAssignment'] = ["test","testtask",0]
    result = self.app.get("/assignment")
    self.assertEqual(result.status_code, 200)

  def test_task_mock_wrong_value(self):
    with self.app.session_transaction() as session:
      session['currentAssignment'] = ["fdsfds","fdsafds",0]
    result = self.app.get("/assignment")
    self.assertEqual(result.location, "http://localhost/")

  def test_task_mock_result(self):
    with self.app.session_transaction() as session:
      session['currentAssignment'] = ["test","testtask",0]
    result = self.app.get("/assignment/True/testwoord")
    self.assertEqual(result.status_code, 200)

  def test_results_load_empty(self):
    result = self.app.get("/results")
    self.assertEqual(result.status_code, 200)

  def test_results_load_filled(self):
    with self.app.session_transaction() as session:
      session['currentScore'] = [2,5]
      session['score'] = [15,6]
    result = self.app.get('/results')
    self.assertEqual(result.status_code, 200)

  def test_clear_removesValues(self):
    with self.app.session_transaction() as session:
      session['currentScore'] = [2,3]
      oldSession = session['currentScore']
    result = self.app.get('/clearSessionStorage')
    with self.app.session_transaction() as session:
      self.assertNotEqual(session['currentScore'], oldSession)

  def test_clear_load(self):
    result = self.app.get('/clearSessionStorage')
    self.assertEqual(result.location, "http://localhost/results")

  def test_about_load(self):
    result = self.app.get('/about')
    self.assertEqual(result.status_code,200)

if __name__ == '__main__':
  unittest.main()


  
