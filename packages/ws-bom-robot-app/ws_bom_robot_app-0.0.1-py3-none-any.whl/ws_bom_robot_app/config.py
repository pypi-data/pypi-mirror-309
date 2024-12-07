from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    robot_env: str = 'local'
    robot_user: str = 'user'
    robot_password: str = 'password'
    robot_data_folder: str = './.data'
    robot_data_db_folder: str = 'vector_db'
    robot_data_db_folder_src: str = 'src'
    robot_data_db_folder_out: str = 'out'
    robot_data_db_folder_store: str = 'store'
    robot_cms_host: str = ''
    robot_cms_auth: str = ''
    robot_cms_db_folder: str = 'llmVectorDb'
    robot_cms_kb_folder: str ='llmKbFile'
    robot_debugger_openai_key: str = ''
    class Config:
        env_file = './.env'
        extra = 'ignore'
        case_sensitive = False

    class RuntimeOptions(BaseModel):
        debug: bool
        loader_strategy: str
        loader_show_progress: bool
        loader_silent_errors: bool


    def runtime_options(self) -> RuntimeOptions:
      """_summary_
      Returns:
          _runtime_options:
            return degug flag and loader options based on the robot environment.
            the loader options is usefull to minimizing sytem requirements/dependencies for local development
      """
      if self.robot_env == "local":
        return self.RuntimeOptions(debug=True,loader_strategy="auto",loader_show_progress=True, loader_silent_errors=True)
      elif self.robot_env == "development":
        return self.RuntimeOptions(debug=True,loader_strategy="",loader_show_progress=True, loader_silent_errors=False)
      else:
        return self.RuntimeOptions(debug=False,loader_strategy="",loader_show_progress=False, loader_silent_errors=True)

# global instance
config = Settings()

