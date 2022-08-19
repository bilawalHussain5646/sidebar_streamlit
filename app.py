import streamlit as st
import streamlit.components.v1 as components
import codecs
from data_managements.dataset_utils import  HF_DESC_FIELD, HF_FEATURE_FIELD, HF_LABEL_FIELD
from data_managements import dataset_utils

with open("style.css") as f:                                                # Reading style.css file and opening it 
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html= True)       # Storing all styles in the streamlit markdown  &   unsafe_allow_html to true so that we can use html tags with the code  
    #----read and run html file




def sidebar_selection(ds_name_to_dict,column_id):

    ds_names = list(ds_name_to_dict.keys())             # Storing keys of the data sent as parameter 
    
    #with st.sidebar.expander(f"Choose dataset and field {column_id}", expanded=True):
    # choose a dataset to analyze
    i=1                                                 # Inorder to start numbering from 1 we initialize and declare i=1 
    expanded= True
    with st.sidebar:                                    # In order to add information or fields we refer to sidebar here 
        st.sidebar.subheader(f"Choose dataset and field {column_id}")               # Creating subheader and displaying message  
        # with st.sidebar.subheader(f"Choose dataset and field {column_id}"):
        st.markdown('<p class="question"><span><span class="number-label">'+str(i)+'</span></span>'+f"<span>Select a dataset to explore{column_id}:</span>"+'</p>',unsafe_allow_html=True)      # Creating markdown to add Question and unsafe_allow_html to True to make the tags displayed
        ds_name = st.selectbox(f"Select a dataset to explore{column_id}:",ds_names,index=ds_names.index("hate_speech18"),)                      # Adding Question and options in the selectbox. NOTE: THIS QUESTION IS STYLED AND SET DISPLAYED TO NONE BECAUSE WE WANT TO USE MARKDOWN AS QUESTION
    # choose a config to analyze
        i+=1            # Increasing question number by 1 
        ds_configs = ds_name_to_dict[ds_name]                   # Saving value of those keys in the ds_configs
        if ds_name == "c4":                                     # if the key is c4 then store   ['en','en.noblocklist','realnewslike']   in the config_names
            config_names = ['en','en.noblocklist','realnewslike']
        else:                                                      # else 
            config_names = list(ds_configs.keys())                  # store all the keys of the selected option and convert it to a list 
        st.markdown('<p class="question"><span><span class="number-label">'+str(i)+'</span></span>'+f"Choose a configuration from the selected dataset{column_id}:"+'</p>',unsafe_allow_html=True) # Creating markdown to add Question and unsafe_allow_html to True to make the tags displayed
        config_name = st.radio(f"Choose a configuration from the selected dataset{column_id}:",config_names,index=0,)  # Adding Question and options in the selectbox. NOTE: THIS QUESTION IS STYLED AND SET DISPLAYED TO NONE BECAUSE WE WANT TO USE MARKDOWN AS QUESTION
        # choose a subset of num_examples
        i+=1            # Increasing question number by 1 
        ds_config = ds_configs[config_name]
        text_features = ds_config[HF_FEATURE_FIELD]["string"]
        st.markdown('<p class="question"><span><span class="number-label">'+str(i)+'</span></span>'+f"Choose a text feature from the{column_id} dataset would you like to analyze?"+'</p>',unsafe_allow_html=True) # Creating markdown to add Question and unsafe_allow_html to True to make the tags displayed

        text_field = st.radio(f"Choose a text feature from the{column_id} dataset would you like to analyze?",[("text",)]   # if ds_name == "c4"   ----> [("text",)]
        if ds_name == "c4"
        else [tp for tp in text_features if tp[0] != "id"],   # Else do this 
        )   # Adding Question and options in the selectbox. NOTE: THIS QUESTION IS STYLED AND SET DISPLAYED TO NONE BECAUSE WE WANT TO USE MARKDOWN AS QUESTION
        # Choose a split and dataset size
        avail_splits = list(ds_config["splits"].keys())   # store all the keys of the selected option and convert it to a list 
        i=i+1               # Next Number of the question 
        if "test" in avail_splits:              # 
            avail_splits.remove("test")
        st.markdown('<p class="question"><span><span class="number-label">'+str(i)+'</span></span>'+f"Choose a split from the{column_id} dataset would you like to analyze?"+'</p>',unsafe_allow_html=True) # Creating markdown to add Question and unsafe_allow_html to True to make the tags displayed
        
        split = st.radio(f"Choose a split from the{column_id} dataset would you like to analyze?",avail_splits,index=0,) # Adding Question and options in the selectbox. NOTE: THIS QUESTION IS STYLED AND SET DISPLAYED TO NONE BECAUSE WE WANT TO USE MARKDOWN AS QUESTION
        label_field, label_names = (ds_name_to_dict[ds_name][config_name][HF_FEATURE_FIELD][HF_LABEL_FIELD][0] if len(ds_name_to_dict[ds_name][config_name][HF_FEATURE_FIELD][HF_LABEL_FIELD])> 0 else ((), []))
        # if len(ds_name_to_dict[ds_name][config_name][HF_FEATURE_FIELD][HF_LABEL_FIELD])> 0    --->  ds_name_to_dict[ds_name][config_name][HF_FEATURE_FIELD][HF_LABEL_FIELD][0]
        # else ---> ((), [])

        st.markdown('<p class="question"></p>',unsafe_allow_html=True) # This is just to cover the line on the frontend

    return {                            # Returning all the values that were taken as input
    "dset_name": ds_name,
    "dset_config": config_name,
    "split_name": split,
    "text_field": text_field,
    "label_field": label_field,
    "label_names": label_names,
    }

def OptionSidebar(data_set):

            with st.sidebar: 
                i=1
                for key,value in data_set.items():    
                    ds_name_input = value
                    key, value = list(ds_name_input.items())[0]
                    optkey, optvalue = list(ds_name_input.items())[1]
                    if optvalue == "selectbox":
                        st.markdown('<p class="question"><span><span class="number-label">'+str(i)+'</span></span>'+str(key)+'</p>',unsafe_allow_html=True)
                        ds_name = st.selectbox(key,(value))
                        
                    else:
                        st.markdown('<p class="question"><span><span class="number-label">'+str(i)+'</span></span>'+str(key)+'</p>',unsafe_allow_html=True)
                        ds_name =st.radio(key,(value))
                    i+=1
data_set = {
        'ds_name': {
                    'How would you like to be contacted? ': ['Email','Home phone','Mobile phone'],
                    'type': 'selectbox' 
        },
        'config_name':{
                    'Choose a configuration from the selected dataset: ': ['Comedy','Drama','Documentary'],
                    'type': 'radio' 
        },
        'text_field': {
                    'Choose a text feature from the dataset would you like to analyze?': ['option 1','option 2'],
                    'type': 'radio' 
        },
        'split': {
                    "Choose a split from the{column_id} dataset would you like to analyze?": ['Music', 'Art', 'Contempoaray'],
                    'type': 'radio' 
        }
}
def main():
    ds_name_to_dict = dataset_utils.get_dataset_info_dicts()  # Get Dataset from the dataset_utils and store in ds_name_to_dict
    print(ds_name_to_dict)          # print dataset 
    rtnValue = sidebar_selection(ds_name_to_dict,"")    # Passing Dataset and column number to the sidebar_selection function 
    
  
if __name__ == "__main__":
#    main()               #calling main function 

# ---------Testing Purpose-----------------------
    



    OptionSidebar(data_set)
    # with open("style.css") as f:                                                # Reading style.css file and opening it 
    #     st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html= True)       # Storing all styles in the streamlit markdown  &   unsafe_allow_html to true so that we can use html tags with the code  
    # #----read and run html file    



# ------------------------------------------------------
