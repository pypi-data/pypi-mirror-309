import os
from ws_bom_robot_app.llm.utils.print import HiddenPrints
from ws_bom_robot_app.llm.utils.faiss_helper import FaissHelper

async def get_rules(rules_folder: str, api_key:str, input: str) -> str:
  with HiddenPrints():
    if input=="" or rules_folder == "" or not os.path.exists(rules_folder):
      return ""
    rules_prompt = ""
    rules_doc = await FaissHelper.invoke(rules_folder,api_key,input,search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.7}) #type: ignore
    if len(rules_doc) > 0:
      rules_prompt = "\nFollow this rules: \n RULES: \n"
      for rule_doc in rules_doc:
        rules_prompt += "- " + rule_doc.page_content + "\n"
    return rules_prompt
