import unittest

from WebPipeline import *
from mockobjects import *

class Test_integration(unittest.TestCase):
  def setUp(self):
    self.injector = Modules.injector
    self.name = []
    for item in self.injector.getModule().module:
      self.name += [item.name]      
    self.assignment = self.injector.getModule().module[0].data[0].name
    self.app = app.test_client()
    self.app.secret_key = os.urandom(24)
    self.app.testing = True

  def test_homepage_load(self):
    result = self.app.get('/')
    self.assertEqual(result.status_code,200)

  def test_correctmodule_load(self):
    for item in self.name:
      result = self.app.get('/module/' + item)
      self.assertEqual(result.status_code,200)

  def test_wrongmodule_load(self):
    result = self.app.get('/module/Verkeerde value')
    self.assertEqual(result.location,"http://localhost/404")

  def test_check_correctValue(self):
    for item in self.name:
      for assignment in Modules.injector.getModule().find(item).data:
        result = self.app.get("/check/" + item + "/" + assignment.name)
        self.assertEqual(result.location,"http://localhost/assignment")

  def test_check_wrong_module_name(self):
    result = self.app.get("/check/Verkeerde value/testtask")
    self.assertEqual(result.location,"http://localhost/404")

  def test_check_wrong_task_name(self):
    result = self.app.get("/check/test/Verkeerde value")
    self.assertEqual(result.location,"http://localhost/404")

  def test_task(self):
    for item in self.name:
      for assignment in Modules.injector.getModule().find(item).data:
        result = currentAssignment("/assignment",[item,assignment.name,0],self)
        self.assertTrue(result)

  def test_task_wrongValue(self):
    result = currentAssignment("/assignment",["Verkeerde value" ,"Verkeerde value",0],self)
    self.assertFalse(result)

  def test_task_result(self):
    for item in self.name:
      for assignment in Modules.injector.getModule().find(item).data:
        result = currentAssignment("/assignment/True/testword",[item,assignment.name,0],self)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()

def currentAssignment(url, sessionValue, app):
  with app.app.session_transaction() as session:
    session['currentAssignment'] = sessionValue
  result = app.app.get(url)
  return (result.status_code == 200)
