import pandas as pd
import requests
from PyWrike.gateways import OAuth2Gateway1
from PyWrike import (
    validate_token,
    authenticate_with_oauth2,
    get_folder_id_by_name,
    get_subfolder_id_by_name,
    create_wrike_project,
    create_wrike_folder,
    delete_wrike_folder,
    delete_wrike_project
)

# Main function to handle project and folder creation and deletion
def create_delete_folders_main():
    excel_file = input("Enter the path to the Excel file: ")
    try:
        config_df = pd.read_excel(excel_file, sheet_name="Config", header=1)
        project_df = pd.read_excel(excel_file, sheet_name="Projects")
    except Exception as e:
        print(f"Failed to read Excel file: {e}")
        return 

    access_token = config_df.at[0, "Token"]
    folder_path = config_df.at[0, "Project Folder Path"]
        # Validate the token
    if not validate_token(access_token):
        # If the token is invalid, authenticate using OAuth2 and update the access_token
        wrike = OAuth2Gateway1(excel_filepath=excel_file)
        access_token = wrike._create_auth_info()  # Perform OAuth2 authentication
        print(f"New access token obtained: {access_token}")
        
    
    parent_folder_id = get_folder_id_by_name(folder_path, access_token)
    if not parent_folder_id:
        print("Parent folder ID not found.")
        return
    print(f"Parent folder ID: {parent_folder_id}")

    # Group rows by project name
    create_projects = project_df[["Create Project Title", "Create Folders"]]
    delete_projects = project_df[["Delete Project Title", "Delete Folders"]]

    # Create projects and folders
    for project_name, group in create_projects.groupby("Create Project Title"):
        print(f"Processing project: {project_name}")
        
        project_id = get_subfolder_id_by_name(parent_folder_id, project_name.strip(), access_token)
        
        if not project_id:
            print(f"Project '{project_name.strip()}' not found. Creating it.")
            project_id = create_wrike_project(access_token, parent_folder_id, project_name.strip())
        else:
            print(f"Project '{project_name.strip()}' found with ID: {project_id}")

        if project_id:
            folders = group["Create Folders"].dropna().tolist()
            if not folders:
                print(f"No folders to create in project '{project_name.strip()}'")
            for folder_name in folders:
                if folder_name.strip():
                    print(f"Creating folder '{folder_name.strip()}' in project '{project_name.strip()}'")
                    create_wrike_folder(access_token, project_id, folder_name.strip())

    # Delete projects and folders
    for project_name, group in delete_projects.groupby("Delete Project Title"):
        print(f"Processing project: {project_name}")

        project_id = get_subfolder_id_by_name(parent_folder_id, project_name.strip(), access_token)
        
        if project_id:
            folders = group["Delete Folders"].dropna().tolist()
            if not folders:
                print(f"No folders to delete in project '{project_name.strip()}'")
            for folder_name in folders:
                if folder_name.strip():
                    print(f"Deleting folder '{folder_name.strip()}' from project '{project_name.strip()}'")
                    delete_wrike_folder(access_token, project_id, folder_name.strip())
            
            # Delete the project itself if folders are not specified or all are deleted
            print(f"Deleting project '{project_name.strip()}' itself")
            delete_wrike_project(access_token, parent_folder_id, project_name.strip())
        else:
            print(f"Project '{project_name.strip()}' not found, skipping deletion.")

if __name__ == '__create_delete_folders_main__':
    create_delete_folders_main()