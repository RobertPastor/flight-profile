import unittest

from trajectory.OutputFiles.XlsxOutputFile import XlsxOutput

class Test_XlsxOutputFile(unittest.TestCase):

    def test_main(self):
        xlsxOutput = XlsxOutput(fileName = 'Xlsx-Output-tests', sheetName="Results")
        Headers = ['One', 'Two', 'Three']
        xlsxOutput.writeHeaders(Headers)
        xlsxOutput.writeTwoFloatValues(time=1.1,
                        firstFloatValue = 9.9,
                        secondFloatValue = 8.8)
        xlsxOutput.close()
        
if __name__ == '__main__':
    unittest.main()