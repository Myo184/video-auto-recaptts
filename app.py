import gradio as gr
from auth import AuthManager
from membership import MembershipManager
from video import VideoProcessor
from sheet import SheetManager
from history import HistoryManager
import os
import shutil
from datetime import datetime
from config import PORT, IS_PRODUCTION, IS_RAILWAY, UPLOAD_FOLDER, OUTPUT_FOLDER

class VideoRecapApp:
    def __init__(self):
        self.auth = AuthManager()
        self.membership = MembershipManager()
        self.sheet = SheetManager()
        self.history = HistoryManager()
        self.current_user = None
        self.video_processor = None
        
        if IS_PRODUCTION:
            print("🚀 Running in Production Mode")
        if IS_RAILWAY:
            print("🚂 Running on Railway.app")
    
    def login(self):
        try:
            user_info = self.auth.login()
            self.current_user = user_info['email']
            self.video_processor = VideoProcessor(self.current_user)
            return f"✅ Logged in as: {self.current_user}"
        except Exception as e:
            return f"❌ Login failed: {str(e)}"
    
    def get_dashboard(self):
        if not self.current_user:
            return "Please login first"
        
        status = self.membership.get_user_status(self.current_user)
        if not status:
            return "User not found"
        
        dashboard = f"""
        ### 👤 Account
        - **Email:** {status['gmail']}
        - **Name:** {status['name']}
        - **Member:** {'✅ Yes' if status['member'] else '❌ No'}
        """
        
        if status['member']:
            dashboard += f"\n- **Remaining Days:** {status['remaining_days']} days"
        
        dashboard += f"""
        - **Videos Today:** {status['today_count']}/{status['daily_limit']}
        - **API Keys:** {len(status['api_keys'])} configured
        - **Status:** {'Active' if status['valid'] else 'Inactive'}
        """
        
        return dashboard
    
    def process_video(self, video_file, logo_file, api_keys, 
                     subtitle_color, subtitle_size, subtitle_position,
                     logo_position, logo_opacity):
        if not self.current_user:
            return None, "Please login first"
        
        access, message = self.membership.check_access(self.current_user)
        if not access:
            return None, message
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            video_filename = f"{timestamp}_{os.path.basename(video_file.name)}"
            video_path = os.path.join(UPLOAD_FOLDER, video_filename)
            shutil.copy(video_file.name, video_path)
            
            logo_path = None
            if logo_file:
                logo_filename = f"logo_{timestamp}.png"
                logo_path = os.path.join(UPLOAD_FOLDER, logo_filename)
                shutil.copy(logo_file.name, logo_path)
            
            if api_keys:
                keys = [k.strip() for k in api_keys.split(',') if k.strip()]
                self.sheet.set_user_api_keys(self.current_user, keys)
            
            self.video_processor = VideoProcessor(self.current_user)
            output_path, status = self.video_processor.process_video(
                video_path,
                logo_path,
                subtitle_color,
                int(subtitle_size),
                subtitle_position,
                logo_position,
                float(logo_opacity)
            )
            
            if output_path and os.path.exists(output_path):
                self.membership.process_video(self.current_user)
                return output_path, "✅ Video processed successfully!"
            else:
                return None, f"❌ Error: {status}"
                
        except Exception as e:
            return None, f"❌ Error: {str(e)}"
    
    def create_ui(self):
        with gr.Blocks(title="Video Recap SaaS", theme=gr.themes.Soft()) as demo:
            gr.Markdown("# 🎬 Video Auto Recap SaaS")
            gr.Markdown("### Myanmar Subtitle + TTS + Logo + Summary")
            
            with gr.Row():
                login_btn = gr.Button("🔐 Login with Google", variant="primary")
                logout_btn = gr.Button("🚪 Logout", variant="secondary")
            
            status_text = gr.Textbox(label="Status", interactive=False)
            dashboard_text = gr.Markdown("**Dashboard will appear here after login**")
            
            with gr.Tabs():
                with gr.TabItem("📤 Upload Video"):
                    with gr.Row():
                        with gr.Column(scale=2):
                            video_input = gr.File(
                                label="Upload Video",
                                file_types=[".mp4", ".avi", ".mov", ".mkv"]
                            )
                            logo_input = gr.File(
                                label="Upload Logo (Optional - PNG)",
                                file_types=[".png", ".jpg", ".jpeg"]
                            )
                            api_keys_input = gr.Textbox(
                                label="Gemini API Keys (comma separated)",
                                placeholder="key1,key2,key3,key4",
                                lines=2
                            )
                            
                            with gr.Row():
                                subtitle_color = gr.ColorPicker(
                                    label="Subtitle Color",
                                    value="#FFFFFF"
                                )
                                subtitle_size = gr.Slider(
                                    label="Subtitle Size",
                                    minimum=20,
                                    maximum=80,
                                    value=40,
                                    step=2
                                )
                            
                            subtitle_position = gr.Radio(
                                label="Subtitle Position",
                                choices=["bottom", "top", "center"],
                                value="bottom"
                            )
                            
                            with gr.Row():
                                logo_position = gr.Dropdown(
                                    label="Logo Position",
                                    choices=["top-left", "top-right", 
                                            "bottom-left", "bottom-right"],
                                    value="top-right"
                                )
                                logo_opacity = gr.Slider(
                                    label="Logo Opacity",
                                    minimum=0.1,
                                    maximum=1.0,
                                    value=0.8,
                                    step=0.1
                                )
                            
                            generate_btn = gr.Button("🚀 Generate Video", variant="primary")
                        
                        with gr.Column(scale=1):
                            output_video = gr.Video(label="Generated Video")
                            output_status = gr.Textbox(label="Status")
                
                with gr.TabItem("📊 History"):
                    history_refresh = gr.Button("🔄 Refresh History")
                    history_table = gr.Dataframe(
                        headers=["Video Name", "Date", "Duration", "Status"],
                        label="Video History"
                    )
                
                with gr.TabItem("👤 Account"):
                    account_status = gr.Markdown()
                    refresh_btn = gr.Button("🔄 Refresh Account")
                
                with gr.TabItem("🔑 API Keys"):
                    api_keys_manage = gr.Textbox(
                        label="Manage API Keys (comma separated)",
                        placeholder="key1,key2,key3"
                    )
                    save_keys_btn = gr.Button("💾 Save API Keys")
                    keys_status = gr.Textbox(label="Status")
            
            login_btn.click(
                self.login,
                outputs=[status_text]
            ).then(
                self.get_dashboard,
                outputs=[dashboard_text]
            )
            
            logout_btn.click(
                lambda: (None, "Logged out"),
                outputs=[status_text, dashboard_text]
            )
            
            generate_btn.click(
                self.process_video,
                inputs=[
                    video_input, logo_input, api_keys_input,
                    subtitle_color, subtitle_size, subtitle_position,
                    logo_position, logo_opacity
                ],
                outputs=[output_video, output_status]
            ).then(
                self.get_dashboard,
                outputs=[dashboard_text]
            )
            
            refresh_btn.click(
                self.get_dashboard,
                outputs=[account_status]
            )
            
            def get_history():
                if self.current_user:
                    return self.history.get_user_history(self.current_user)
                return []
            
            history_refresh.click(
                get_history,
                outputs=[history_table]
            )
            
            def save_keys(keys):
                if not self.current_user:
                    return "Please login first"
                keys_list = [k.strip() for k in keys.split(',') if k.strip()]
                self.sheet.set_user_api_keys(self.current_user, keys_list)
                return f"✅ Saved {len(keys_list)} API keys"
            
            save_keys_btn.click(
                save_keys,
                inputs=[api_keys_manage],
                outputs=[keys_status]
            )
            
            demo.load(
                self.get_dashboard,
                outputs=[dashboard_text]
            )
        
        return demo

if __name__ == "__main__":
    app = VideoRecapApp()
    demo = app.create_ui()
    
    demo.launch(
        server_name="0.0.0.0", 
        server_port=PORT,
        share=False,
        debug=not IS_PRODUCTION
    )
