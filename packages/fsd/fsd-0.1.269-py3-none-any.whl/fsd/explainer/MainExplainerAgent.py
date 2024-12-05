import os
import sys
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
from fsd.util.utils import process_image_files
logger = get_logger(__name__)

class MainExplainerAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    def read_all_file_content(self, all_path):
        all_context = ""

        for path in all_path:
            file_context = read_file_content(path)
            all_context += f"\n\nFile: {path}\n{file_context}"

        return all_context

    async def get_answer_plan(self, conversation_history, user_prompt, language, all_file_content, role, file_attachments, focused_files, assets_link, crawl_logs):
        prompt = ""
        all_attachment_file_contents = ""
        all_focused_files_contents = ""

        # Process image files
        image_files = process_image_files(file_attachments)
        
        # Remove image files from file_attachments
        file_attachments = [f for f in file_attachments if not f.lower().endswith(('.webp', '.jpg', '.jpeg', '.png'))]

        if file_attachments:
            for file_path in file_attachments:
                file_content = read_file_content(file_path)
                if file_content:
                    all_attachment_file_contents += f"\n\nFile: {os.path.relpath(file_path)}:\n{file_content}"

        if focused_files:
            for file_path in focused_files:
                file_content = read_file_content(file_path)
                if file_content:
                    all_focused_files_contents += f"\n\nFile: {os.path.relpath(file_path)}:\n{file_content}"

        if crawl_logs:
            prompt += f"\nThis is supported data for this entire process, use it if appropriate: {crawl_logs}"

        if all_attachment_file_contents:
            prompt += f"\nUser has attached these files for you, use them appropriately: {all_attachment_file_contents}"

        if all_focused_files_contents:
            prompt += f"\nUser has focused on these files in the current project, pay special attention to them according to user prompt: {all_focused_files_contents}"


        prompt += (
            f"Current time, only use if need: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo}"
            f"Context:\n{all_file_content}\n"
            f"User prompt:\n{user_prompt}\n"
            f"Project tree, only use if need: {self.repo.print_tree()}\n"
            "DO NOT PROVIDE FULL TREE, ONLY IF USER IS ASKING FOR IT"
            "ONLY PROVIDE TREE WHEN REALLY NEEDED, OTHERWISE DON'T PROVIDE TREE SINCE IT'S NOT RELEVANT AND WASTE TOKEN"
            "FOR ALL CODING-RELATED RESPONSES: FOCUS ON CONCISE, KEY CODE EXAMPLES RATHER THAN FULL IMPLEMENTATIONS. BE AS SUCCINCT AS POSSIBLE WHILE MAINTAINING CLARITY. YOU ARE A CODE ANALYST, NOT A PROGRAMMER. PROVIDE A COMPREHENSIVE ANALYSIS WITH SPECIFIC, ACTIONABLE FEEDBACK AND RECOMMENDATIONS."
            "ONLY PROVIDE EXTENSIVE CODE SNIPPETS IF THE USER EXPLICITLY AND DIRECTLY REQUESTS THEM."
            "FOR EACH FILE YOU WORK ON USER TASKS, YOU NEED TO CLEARLY MENTION THE PATH AND FILENAME OF EACH ONE YOU PROVIDE. THE USER NEEDS TO KNOW THE LOCATION TO REVIEW YOUR SOLUTION."
            f"Respond in this language:\n{language}\n"
        )

        user_content = [{"type": "text", "text": prompt}]

        # Add image files to the user content
        for base64_image in image_files:
            user_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"{base64_image}"
                }
            })

        if assets_link:
            for image_url in assets_link:
                user_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                })

        conversation_history.append({
            "role": "user",
            "content": user_content
        })

        try:
            logger.info(f" #### The `{role}` is in charge.\n")
            res = await self.ai.explainer_stream_prompt(conversation_history, 4096, 0.2, 0.1)
            conversation_history.append({"role": "assistant", "content": res})
            
            # Keep conversation history no longer than 30 pairs, excluding the system prompt
            if len(conversation_history) > 61:  # 1 system + 30 user/assistant pairs
                conversation_history = conversation_history[:1] + conversation_history[-60:]
            
            return conversation_history
        except Exception as e:
            logger.error(f"  The `{role}` encountered some errors")
            # Remove the last user prompt from history in case of error
            if len(conversation_history) > 1 and conversation_history[-1]["role"] == "user":
                conversation_history.pop()
            return conversation_history

    async def get_answer_plans(self, conversation_history, user_prompt, language, files, role, file_attachments, focused_files, assets_link, crawl_logs):
        files = [file for file in files if file]

        all_path = files
        logger.debug("\n #### `File Aggregator Agent`: Commencing file content aggregation for analysis")
        all_file_content = self.read_all_file_content(all_path)

        logger.debug("\n #### `Answer Plan Generator`: Initiating answer plan generation based on user input")
        plan = await self.get_answer_plan(conversation_history, user_prompt, language, all_file_content, role, file_attachments, focused_files, assets_link, crawl_logs)
        return plan
