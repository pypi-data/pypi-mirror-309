from flask import Blueprint, request, jsonify, send_file
from abstract_utilities import *
from abstract_pandas import *
import os
def getAbsPath():
  return os.path.dirname(os.path.abspath(__name__))
def makeAbsFile(path):
  return os.path.join(getAbsPath(),path)
def get_solanaTrackDir():
  trackerDir = makeAbsFile('solanaTrackDir')
  os.makedirs(trackerDir,exist_ok=True)
  return trackerDir
def get_solanaDfPath():
  return os.path.join(get_solanaTrackDir(),'solanaTracker.xlsx')
def getSolanaDfData():
  solanaDfPath = get_solanaDfPath()
  if not os.path.isfile(solanaDfPath):
    safe_excel_save(get_df([{}]),solanaDfPath)
  return get_df(solanaDfPath)
  
input(getSolanaDfData())
solana_tracker = Blueprint('solana_tracker', __name__)

# Directory to save the master Excel record
EXCEL_DIR = '/path/to/your/excel/files'
EXCEL_FILE = os.path.join(EXCEL_DIR, 'solana_swaps_master.xlsx')

@solana_tracker.route('/track_swap', methods=['POST'])
def track_swap():
    data = request.json
    
    # Assuming `data` contains relevant swap details
    swap_df = pd.DataFrame([data])
    
    # Check if the master Excel file exists
    if os.path.exists(EXCEL_FILE):
        master_df = pd.read_excel(EXCEL_FILE)
        master_df = pd.concat([master_df, swap_df], ignore_index=True)
    else:
        master_df = swap_df
    
    # Save the updated dataframe to Excel
    master_df.to_excel(EXCEL_FILE, index=False)
    
    return jsonify({"message": "Swap tracked successfully"}), 201

@solana_tracker.route('/get_swaps', methods=['GET'])
def get_swaps():
    if os.path.exists(EXCEL_FILE):
        return send_file(EXCEL_FILE, as_attachment=True)
    else:
        return jsonify({"message": "No swaps tracked yet."}), 404
