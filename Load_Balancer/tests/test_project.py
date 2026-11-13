import ast, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ProjectChecks(unittest.TestCase):
    def test_files(self):
        for name in ("server.py","load_balancer.py","requirements.txt","README.txt","Project_Report.docx"):
            self.assertTrue((ROOT/name).is_file(),name)
    def test_syntax(self):
        for name in ("server.py","load_balancer.py"):
            ast.parse((ROOT/name).read_text(encoding="utf-8"))
    def test_load_balancer_features(self):
        text=(ROOT/"load_balancer.py").read_text(encoding="utf-8")
        for term in ("Round Robin","/api/status","/dashboard","server_is_healthy","503"):
            self.assertIn(term,text)
if __name__=="__main__": unittest.main()
