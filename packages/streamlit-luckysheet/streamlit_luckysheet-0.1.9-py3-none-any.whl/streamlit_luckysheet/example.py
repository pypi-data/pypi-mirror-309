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

# # Configuration constants
# name = "Streamlit_Excelsheet"
# key = "Streamlit_Excelsheet"
# height = 1000
# file_name = "Config_Test_Output1"
# file_path_dir = ".\\excel\\"
# save_path = file_path_dir + file_name
# file_type = None

# # File paths and configurations for testing
# # Uncomment to test different file sizes
# # file_path = r".\excel\SampleDocs-SampleXLSFile_6800kb.xlsx" 
# # save_path = r'.\{excel}\.' + file_name

# # Speed Test Logs (Excel sheet size and time performance)
# # Speed 400kRow9Column.xlsx 25,430 KB | Time out
# # Speed 400kRow9Column_Reduce.xlsx 20,129 KB | Time out @ 1:53.94
# # Speed 200kRow9Column.xlsx 15,680 KB | 1min 03.30
# # Speed 100kRow9Column.xlsx 10,806 KB | 30.67
# # Speed 50kRow9Column.xlsx 3,192 KB | 16.12


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
#                 return json.load(file)  # Parse the JSON file and return as a Python object
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


# # Convert Base64 data into an Excel or file format

# # Convert Base64 JSON data back into a file
# # def base64_to_file(sheetsBase64, save_path):
# #     try:
# #         decoded_data = base64.b64decode(sheetsBase64["data_chunks"])
# #         # json_data = json.loads(decoded_data.decode("utf-8"))
# #         # st.warning(decoded_data)
# #         with open(save_path, 'ab') as json_string:
# #             json_string.write(decoded_data)
# #             # json.dump(decoded_data, json_string, indent=4)
# #         # json_string.close()
# #     except Exception as e:
# #         st.warning(f"An error occurred while converting to JSON file: {e}")


# #############################################################################
# def handle_chunk_file(fragment, save_path, option):
#     if "chunks" not in st.session_state:
#         st.session_state["chunks"] = []
#     st.session_state["chunks"].append(fragment['data_chunks'])
#     if fragment['index_chunks'] ==  fragment['total_chunks'] - 1:
#         st.info(f"All { fragment['total_chunks']} chunks received. Saving file...")
#         incoming_base64 = ''.join(st.session_state["chunks"])
#         match option:
#             case "json":
#                 base64_to_json(incoming_base64, save_path)
#             case "xlsx":
#                 base64_to_file(incoming_base64, save_path)
#         del st.session_state["chunks"]
#         time.sleep(0.1)
        

# def base64_to_file(base64_string, save_path):
#     try:
#         output_dir = os.path.dirname(save_path)
#         if not os.path.exists(output_dir):
#             os.makedirs(output_dir)
#         decoded_data = base64.b64decode(base64_string)
#         with open(save_path, 'ab') as file:
#             file.write(decoded_data)   
        
#         now = datetime.now()
#         dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#         st.toast(f"[{dt_string}] File successfully created at: {save_path}")
    
#     except Exception as e:
#         st.warning(f"An error occurred while converting to Excel file: {e}")
# #############################################################################

# # Convert Base64 JSON data back into a file
# def base64_to_json(base64_string, save_path):
#     try:
#         output_dir = os.path.dirname(save_path)
#         if not os.path.exists(output_dir):
#             os.makedirs(output_dir)
#         decoded_data = base64.b64decode(base64_string)
#         decompressed_data = zlib.decompress(decoded_data, zlib.MAX_WBITS | 16)

#         json_data = json.loads(decompressed_data.decode('utf-8'))
#         with open(save_path, 'w') as file:
#             json.dump(json_data, file, indent=4)
        
#         now = datetime.now()
#         dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#         st.toast(f"[{dt_string}] File successfully created at: {save_path}")
    
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




# # def base64_to_json(sheetsBase64, save_path):
# #     try:
# #         decoded_data = base64.b64decode(sheetsBase64["data_chunks"])
# #         with open(save_path, 'ab') as json_string:
# #             json_string.write(decoded_data)
# #         st.rerun()
# #     except Exception as e:
# #         st.warning(f"An error occurred while converting to JSON file: {e}")


# # Main program logic starts here
# with st.spinner():
#     file_path, file_type = get_latest_file(file_path_dir)
#     file = read_file(file_path + file_type) if file_path and file_type else None

#     # Debugging & Testing
#     st.warning(file_path) 
#     st.warning(file_type)
#     time.sleep(0.1)

# # Configuration for Luckysheet toolbar
# showtoolbarConfig = {
#     "save": True,
#     "download": False,
#     "undoRedo": True,
#     "paintFormat": True,
#     "currencyFormat": False,
#     "percentageFormat": False,
#     "numberDecrease": False,
#     "numberIncrease": False,
#     "moreFormats": False,
#     "font": True,
#     "fontSize": True,
#     "bold": True,
#     "italic": True,
#     "strikethrough": True,
#     "underline": True,
#     "textColor": True,
#     "fillColor": True,
#     "border": True,
#     "mergeCell": True,
#     "horizontalAlignMode": True,
#     "verticalAlignMode": True,
#     "textWrapMode": True,
#     "textRotateMode": True,
#     "image": False,
#     "link": False,
#     "chart": False,
#     "postil": False,
#     "pivotTable": False,
#     "function": False,
#     "frozenMode": False,
#     "sortAndFilter": False,
#     "conditionalFormat": False,
#     "dataVerification": False,
#     "splitColumn": False,
#     "screenshot": False,
#     "findAndReplace": False,
#     "protection": False,
#     "print": False,
#     "exportXlsx": False,
# }

# # Execute the Luckysheet component and handle results
# return_result = streamlit_luckysheet(name=name, height=height, file=file, file_type=file_type, showtoolbarConfig=showtoolbarConfig, key=key, default=[])

# # Handle the returned result (saving files)
# if isinstance(return_result, dict):
#     if "output_xlsx" in return_result:
#         handle_chunk_file(return_result["output_xlsx"], save_path + "_output_xlsx.xlsx", "xlsx")
#     if "output_json" in return_result:
#         handle_chunk_file(return_result["output_json"], save_path + "_output_json.json", "json")


import streamlit as st
from streamlit_luckysheet import streamlit_luckysheet
import base64
import zlib
import os
import json
import time
from datetime import datetime
import gc

# Set Streamlit page configuration
st.set_page_config(layout="wide")
st.subheader("Component with constant args")

# Declare constants
name = "Streamlit_Excelsheet"
key = "Streamlit_Excelsheet"
height = 1000
file_name = "Config_Test_Output1"
file_path_dir = ".\\excel\\"
save_path = file_path_dir + file_name
file_type = None

# Convert Excel file to Base64
def excel_to_file(path):
    if not os.path.exists(path):
        return ""
    try:
        with open(path, 'rb') as file:
            file_data = file.read()
            if file_data:
                return base64.b64encode(file_data).decode('utf-8')
            else:
                st.warning("File is empty or could not be read.")
                return ""
    except Exception as e:
        st.warning(f"An error occurred while processing the file: {e}")
        return ""


# Read file or JSON data
def read_file(path):
    if not os.path.exists(path):
        return ""
    
    try:
        if path.endswith(".json"):
            with open(path, 'r') as file:
                return json.load(file)
        else:
            with open(path, 'rb') as file:
                file_data = file.read()
                if file_data:
                    return file_data
                else:
                    st.warning("File is empty or could not be read.")
                    return None
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
        return None


def handle_chunk_file(fragment, save_path, option):
    if "chunks" not in st.session_state:
        st.session_state["chunks"] = []
    # Only append if the chunk is new
    if len(st.session_state["chunks"]) < fragment['total_chunks']:
        st.session_state["chunks"].append(fragment['data_chunks'])

    # Process the file once all chunks are received
    if fragment['index_chunks'] == fragment['total_chunks'] - 1:
        st.info(f"All {fragment['total_chunks']} chunks received. Saving file...")
        incoming_base64 = ''.join(str(st.session_state["chunks"]))
        match option:
            case "json":
                base64_to_json(incoming_base64, save_path)
            case "xlsx":
                base64_to_file(incoming_base64, save_path)

        # Clean up and trigger garbage collection to free memory
        del st.session_state["chunks"]
        # gc.collect()  # Force garbage collection
        time.sleep(0.1)  # Slight delay for UI

# Convert Base64 JSON data back into a file
def base64_to_json(base64_string, save_path):
    try:
        # output_dir = os.path.dirname(save_path)
        # if not os.path.exists(output_dir):
        #     os.makedirs(output_dir)

        # if os.path.exists(save_path):
        #     os.remove(save_path)

        decoded_data = base64.b64decode(base64_string)
        decompressed_data = zlib.decompress(decoded_data, zlib.MAX_WBITS | 16)

        json_data = json.loads(decompressed_data.decode('utf-8'))
        with open(save_path, 'w') as file:
            json.dump(json_data, file, indent=4)
        time.sleep(10)  # Small delay to allow file system to settle
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        st.toast(f"[{dt_string}] JSON file successfully created at: {save_path}")
        
        # Free memory
        # gc.collect()  # Force garbage collection after handling data

    except Exception as e:
        st.warning(f"An error occurred while converting to JSON file: {e}")


# Convert Base64 Excel data back into a file
def base64_to_file(base64_string, save_path):
    try:
        # output_dir = os.path.dirname(save_path)
        # if os.path.exists(output_dir):
        #     os.remove(output_dir)

        if os.path.exists(save_path):
            os.remove(save_path)
        
        decoded_data = base64.b64decode(base64_string)
        st.warning(len(decoded_data))
        with open(save_path, 'wb+') as file:
            file.write(decoded_data)

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        st.toast(f"[{dt_string}] File successfully created at: {save_path}")

        # Free memory
        # gc.collect()  # Force garbage collection after handling data
    
    except Exception as e:
        st.warning(f"An error occurred while converting to Excel file: {e}")


# Get the latest modified file in the directory
def get_latest_file(directory):
    try:
        files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        if not files:
            return None, None
        latest_file = max(files, key=os.path.getmtime)
        file_path, file_type = os.path.splitext(latest_file)
        return file_path, file_type
    except Exception as e:
        st.warning(f"An error occurred while finding the latest file: {e}")
        return None, None


# Main program logic starts here
def create_component():
    with st.spinner():
        file_path, file_type = get_latest_file(file_path_dir)
        file = read_file(file_path + file_type) if file_path and file_type else None

        # Debugging & Testing
        st.warning(file_path)
        st.warning(file_type)
        time.sleep(0.1)


    # Configuration for Luckysheet toolbar
    showtoolbarConfig = {
        "save": True,
        "download": False,
        "undoRedo": True,
        # Other toolbar configurations...
    }

    # Execute the Luckysheet component and handle results
    return_result = streamlit_luckysheet(
        name=name,
        height=height,
        file=file,
        file_type=file_type,
        showtoolbarConfig=showtoolbarConfig,
        export_json=True,
        export_excel=True,
        customFun_saveAllExcel=None,
        custFun_saveAllJson=None,
        timeout_delay=5000,
        key=key,
        default=[]
    )
    file = None
    file_type=None
    # Handle the returned result (saving files)
    if isinstance(return_result, dict):
        if "output_xlsx" in return_result:
            handle_chunk_file(return_result["output_xlsx"], save_path + "_output_xlsx.xlsx", "xlsx")
        if "output_json" in return_result:
            handle_chunk_file(return_result["output_json"], save_path + "_output_json.json", "json")

create_component()