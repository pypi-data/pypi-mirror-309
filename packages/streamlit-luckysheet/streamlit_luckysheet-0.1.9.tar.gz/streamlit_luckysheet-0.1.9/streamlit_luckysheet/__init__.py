import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "streamlit_luckysheet",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_luckysheet", path=build_dir)


def streamlit_luckysheet(name="",height=0, file=None, file_type=None, showtoolbarConfig={
        "save": True,
        "download": True,
        "undoRedo": True,
        "paintFormat": True,
        "currencyFormat": False,
        "percentageFormat": False,
        "numberDecrease": False,
        "numberIncrease": False,
        "moreFormats": False,
        "font": True,
        "fontSize": True,
        "bold": True,
        "italic": True,
        "strikethrough": True,
        "underline": True,
        "textColor": True,
        "fillColor": True,
        "border": True,
        "mergeCell": True,
        "horizontalAlignMode": True,
        "verticalAlignMode": True,
        "textWrapMode": True,
        "textRotateMode": True,
        "image": False,
        "link": False,
        "chart": False,
        "postil": False,
        "pivotTable": False,
        "function": False,
        "frozenMode": False,
        "sortAndFilter": False,
        "conditionalFormat": False,
        "dataVerification": False,
        "splitColumn": False,
        "screenshot": False,
        "findAndReplace": False,
        "protection": False,
        "print": False,
        "exportXlsx": False,
      },export_json=False,export_excel=True, customFun_saveAllExcel=None,
      custFun_saveAllJson=None, timeout_delay=1000, key="", default=0):
    component_value = _component_func(name=name,height=height, file=file, file_type=file_type, showtoolbarConfig=showtoolbarConfig, export_json=export_json,export_excel=export_excel,customFun_saveAllExcel=customFun_saveAllExcel,
      custFun_saveAllJson=custFun_saveAllJson, timeout_delay=timeout_delay, key=key, default=default)
    return component_value


# import streamlit as st
# from streamlit_luckysheet import streamlit_luckysheet
# import base64
# import zlib
# import os
# import json
# import time
# from datetime import datetime
# import gc

# # Set Streamlit page configuration
# st.set_page_config(layout="wide")
# st.subheader("Component with constant args")

# # Declare constants
# name = "Streamlit_Excelsheet"
# key = "Streamlit_Excelsheet"
# height = 1000
# file_name = "Config_Test_Output1"
# file_path_dir = ".\\excel\\"
# save_path = file_path_dir + file_name
# file_type = None

# # Convert Excel file to Base64
# def excel_to_file(path):
#     if not os.path.exists(path):
#         return ""
#     try:
#         with open(path, 'rb') as file:
#             file_data = file.read()
#             if file_data:
#                 return base64.b64encode(file_data).decode('utf-8')
#             else:
#                 st.warning("File is empty or could not be read.")
#                 return ""
#     except Exception as e:
#         st.warning(f"An error occurred while processing the file: {e}")
#         return ""


# # Read file or JSON data
# def read_file(path):
#     if not os.path.exists(path):
#         return ""
    
#     try:
#         if path.endswith(".json"):
#             with open(path, 'r') as file:
#                 return json.load(file)
#         else:
#             with open(path, 'rb') as file:
#                 file_data = file.read()
#                 if file_data:
#                     return file_data
#                 else:
#                     st.warning("File is empty or could not be read.")
#                     return None
#     except Exception as e:
#         st.error(f"An error occurred while reading the file: {e}")
#         return None


# def handle_chunk_file(fragment, save_path, option):
#     if "chunks" not in st.session_state:
#         st.session_state["chunks"] = []
#     # Only append if the chunk is new
#     if len(st.session_state["chunks"]) < fragment['total_chunks']:
#         st.session_state["chunks"].append(fragment['data_chunks'])

#     # Process the file once all chunks are received
#     if fragment['index_chunks'] == fragment['total_chunks'] - 1:
#         st.info(f"All {fragment['total_chunks']} chunks received. Saving file...")
#         incoming_base64 = ''.join(st.session_state["chunks"])
#         match option:
#             case "json":
#                 base64_to_json(incoming_base64, save_path)
#             case "xlsx":
#                 base64_to_file(incoming_base64, save_path)

#         # Clean up and trigger garbage collection to free memory
#         st.session_state["chunks"] = []
#         gc.collect()  # Force garbage collection
#         time.sleep(0.1)  # Slight delay for UI

# # Convert Base64 JSON data back into a file
# def base64_to_json(base64_string, save_path):
#     try:
#         # output_dir = os.path.dirname(save_path)
#         # if not os.path.exists(output_dir):
#         #     os.makedirs(output_dir)

#         if os.path.exists(save_path):
#             os.remove(save_path)

#         decoded_data = base64.b64decode(base64_string)
#         decompressed_data = zlib.decompress(decoded_data, zlib.MAX_WBITS | 16)

#         json_data = json.loads(decompressed_data.decode('utf-8'))
#         with open(save_path, 'w') as file:
#             json.dump(json_data, file, indent=4)
#         time.sleep(10)  # Small delay to allow file system to settle
#         now = datetime.now()
#         dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#         st.toast(f"[{dt_string}] JSON file successfully created at: {save_path}")
        
#         # Free memory
#         gc.collect()  # Force garbage collection after handling data

#     except Exception as e:
#         st.warning(f"An error occurred while converting to JSON file: {e}")


# # Convert Base64 Excel data back into a file
# def base64_to_file(base64_string, save_path):
#     try:
#         # output_dir = os.path.dirname(save_path)
#         # if os.path.exists(output_dir):
#         #     os.remove(output_dir)

#         if os.path.exists(save_path):
#             os.remove(save_path)
        
#         decoded_data = base64.b64decode(base64_string)
#         st.warning(len(decoded_data))
#         with open(save_path, 'wb+') as file:
#             file.write(decoded_data)

#         now = datetime.now()
#         dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#         st.toast(f"[{dt_string}] File successfully created at: {save_path}")

#         # Free memory
#         gc.collect()  # Force garbage collection after handling data
    
#     except Exception as e:
#         st.warning(f"An error occurred while converting to Excel file: {e}")


# # Get the latest modified file in the directory
# def get_latest_file(directory):
#     try:
#         files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
#         if not files:
#             return None, None
#         latest_file = max(files, key=os.path.getmtime)
#         file_path, file_type = os.path.splitext(latest_file)
#         return file_path, file_type
#     except Exception as e:
#         st.warning(f"An error occurred while finding the latest file: {e}")
#         return None, None


# # Main program logic starts here
# def create_component():
#     with st.spinner():
#         file_path, file_type = get_latest_file(file_path_dir)
#         file = read_file(file_path + file_type) if file_path and file_type else None

#         # Debugging & Testing
#         st.warning(file_path)
#         st.warning(file_type)
#         time.sleep(0.1)


#     # Configuration for Luckysheet toolbar
#     showtoolbarConfig = {
#         "save": True,
#         "download": False,
#         "undoRedo": True,
#         # Other toolbar configurations...
#     }

#     # Execute the Luckysheet component and handle results
#     return_result = streamlit_luckysheet(
#         name=name,
#         height=height,
#         file=file,
#         file_type=file_type,
#         showtoolbarConfig=showtoolbarConfig,
#         export_json=True,
#         export_excel=True,
#         timeout_delay=1500,
#         key=key,
#         default=[]
#     )

#     # Handle the returned result (saving files)
#     if isinstance(return_result, dict):
#         if "output_xlsx" in return_result:
#             handle_chunk_file(return_result["output_xlsx"], save_path + "_output_xlsx.xlsx", "xlsx")
#         if "output_json" in return_result:
#             handle_chunk_file(return_result["output_json"], save_path + "_output_json.json", "json")

# create_component()