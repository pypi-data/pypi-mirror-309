#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.3.4 Fix duplicate commands in /help command"

import asyncio
from functools import wraps
import logging
import os
from pathlib import Path
import sys
from typing import Dict, Optional, List
from dotenv import load_dotenv
import dotenv

import yaml
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler as TelegramCommandHandler, ContextTypes, PicklePersistence, CallbackContext, filters
from telegram.constants import ParseMode

from .handlers import CommandHandler
from .settings import Settings

from pathlib import Path
import os
import sys

# import bot.util_decorators as util_decorators

logger = logging.getLogger(__name__)

def get_main_script_path() -> Path:
    return (Path(os.path.abspath(sys.modules['__main__'].__file__)))

def get_config_path(config_filename: str = "config.yml") -> Path:
    config_path = get_main_script_path()
    return config_path.parent / config_filename

class TelegramBotFramework:
    
    def with_typing_action(handler):
        @wraps(handler)
        async def wrapper(self, update: Update, context: CallbackContext, *args, **kwargs):
            try:
                logger.debug("Sending typing action")
                await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
                return await handler(self, update, context, *args, **kwargs)
            except Exception as e:
                logger.error(f"Error: {e}")
                return await handler(self, update, context, *args, **kwargs)
        return wrapper

    def with_log_admin(handler):
        @wraps(handler)
        async def wrapper(self, update: Update, context: CallbackContext, *args, **kwargs):
            
            try:
                user_id = update.effective_user.id
                user_name = update.effective_user.full_name
                command = update.message.text
                
                if int(user_id) not in self.admin_users:                    
                    for admin_user_id in self.admin_users:
                        try:
                                log_message = f"Command: {command}\nUser ID: {user_id}\nUser Name: {user_name}"
                                logger.debug(f"Sending log message to admin: {log_message}")                            
                                await context.bot.send_message(chat_id=admin_user_id, text=log_message, parse_mode=ParseMode.MARKDOWN)
                        except Exception as e:
                            logger.error(f"Failed to send log message to admin {admin_user_id}: {e}")

                return await handler(self, update, context, *args, **kwargs)
                
            except Exception as e:
                logger.error(f"Error: {e}")
                return await handler(self, update, context, *args, **kwargs)
        return wrapper

    def with_register_user(handler):
        @wraps(handler)
        async def wrapper(self, update: Update, context: CallbackContext, *args, **kwargs):
            try:
                user_id = update.effective_user.id
                user_data = {
                    'user_id': user_id,
                    'username': update.effective_user.username,
                    'first_name': update.effective_user.first_name,
                    'last_name': update.effective_user.last_name,
                    'language_code': update.effective_user.language_code,
                    'last_message': update.message.text if not update.message.text.startswith('/') else None,
                    'last_command': update.message.text if update.message.text.startswith('/') else None,
                    'last_message_date': update.message.date if not update.message.text.startswith('/') else None,
                    'last_command_date': update.message.date if update.message.text.startswith('/') else None
                }

                # Update or insert persistent user data with user_data dictionary
                await context.application.persistence.update_user_data(user_id, user_data)            
                
                # update or insert each item of user_data dictionary in context
                for key, value in user_data.items():
                    context.user_data[key] = value
                
                # flush all users data to persistence
                await context.application.persistence.flush()
                
                # re-read all users data from persistence to check if data is stored correctly
                all_users_data = await context.application.persistence.get_user_data()
                this_user_data = context.user_data

                return await handler(self, update, context, *args, **kwargs)
            
            except Exception as e:
                logger.error(f"Error in with_persistent_user_data: {e}")
                return await handler(self, update, context, *args, **kwargs)
            
        return wrapper
    
    def __init__(self, token: str = None, admin_users: List[int] = [], config_filename: str = get_config_path(), env_file: Path = None):        
        
        self.logger = logging.getLogger(__name__)
        
        # Get the path of the main executed script
        main_script_path = get_main_script_path()
        self.logger.debug(f"The main script folder path is: {main_script_path}")                
        
        # Get bot token from environment but overwrite it if it is provided inside .env file
        self.env_file = main_script_path.parent / ".env" or env_file
        load_dotenv(override=True, dotenv_path=str(self.env_file))
        env_token = os.getenv("DEFAULT_BOT_TOKEN")
        if not env_token:
            raise ValueError("DEFAULT_BOT_TOKEN not found in environment variables")
        
        self.token = token if token else env_token
        self.admin_users = list(map(int, dotenv.get_key(dotenv.find_dotenv(), "ADMIN_ID_LIST").split(','))) or admin_users
        
        self.config_path = config_filename
        self.settings = Settings()
        self.commands: Dict[str, CommandHandler] = {}
        
        self.app: Optional[Application] = None
        self.registered_handlers = {}
        
        self._load_config()
        self._setup_logging()
        self._register_default_commands()

    def _load_config(self) -> None:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        # 'charmap' codec can't decode byte 0x8f in position 438: character maps to <undefined>
        with open(self.config_path, encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

    def _setup_logging(self) -> None:
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)

    def _register_default_commands(self) -> None:
        command_configs = self.config['bot']['commands']
        
        for cmd_name, cmd_config in command_configs.items():
            self.register_command(
                cmd_name,
                cmd_config['description'],
                cmd_config['response']
            )

    def register_command(self, name: str, description: str, response: str) -> None:
        self.commands[name] = CommandHandler(name, description, response)

    @with_typing_action
    @with_log_admin
    @with_register_user
    async def handle_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Generic handler for bot commands

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        
        try:
            command = update.message.text.split()[0][1:]  # Remove the '/' prefix
            handler = self.commands.get(command)
            
            if handler:
                # TODO: pass the user to filter the help command
                response = await handler.get_response(self, update, context)
                await update.message.reply_text(response)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            error_message = f"Error getting user data in {fname} at line {exc_tb.tb_lineno}: {e}"
            self.logger.error(error_message)               
            await update.message.reply_text(error_message, parse_mode=None)

    @with_typing_action
    @with_log_admin
    @with_register_user
    async def handle_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Configure bot settings

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        
        settings_str = self.settings.display()
        await update.message.reply_text(f"⚙️ Bot Settings:\n{settings_str}")

    @with_typing_action
    @with_log_admin
    @with_register_user
    async def handle_list_commands(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """List available commands

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        
        try:
            logging.info("Listing available commands")
            commands_list = "\n".join(
                f"/{cmd} - {handler.description}"
                for cmd, handler in self.commands.items()
            )
            await update.message.reply_text(f"Available commands:\n{commands_list}")
        except Exception as e:
            self.logger.error(f"Error listing commands: {e}")
            await update.message.reply_text("An error occurred while listing commands.")

    @with_typing_action 
    @with_log_admin
    @with_register_user
    async def cmd_git(self, update: Update, context: CallbackContext):
        """Update the bot's version from a git repository"""
        
        try:
            # get the branch name from the message
            # branch_name = update.message.text.split(' ')[1]
            message = f"_Updating the bot's code from the branch..._" # `{branch_name}`"
            self.logger.info(message)
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
            
            # update the bot's code
            # command = f"git fetch origin {branch_name} && git reset --hard origin/{branch_name}"
            command = "git status"
            
            if len(update.effective_message.text.split(' ')) > 1:
                git_command = update.effective_message.text.split(' ')[1]
                self.logger.info(f"git command: {command}")
                command = f"git {git_command}"
            
            # execute system command and return the result
            # os.system(command=command)
            result = os.popen(command).read()
            self.logger.info(f"Result: {result}")
            
            result = f"_Result:_ `{result}`"
            
            await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            self.logger.error(f"Error: {e}")
            await update.message.reply_text(f"An error occurred: {e}")

    @with_typing_action
    @with_log_admin
    @with_register_user
    async def restart_bot(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Command to restart the bot

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        
        try:
            await update.message.reply_text("_Restarting..._", parse_mode=ParseMode.MARKDOWN)
            args = sys.argv[:]
            args.insert(0, sys.executable)
            os.chdir(os.getcwd())
            os.execv(sys.executable, args)
            
        except Exception as e:
            self.logger.error(f"Error restarting bot: {e}")
            await update.message.reply_text(f"An error occurred while restarting the bot: {e}")

    @with_typing_action 
    @with_log_admin
    @with_register_user
    async def stop_bot(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Command to stop the bot

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
        """
        
        try:
            await update.message.reply_text(f"*{update._bot.username} STOPPED!*", parse_mode=ParseMode.MARKDOWN)

            args = sys.argv[:]
            args.insert(0, 'stop')
            args = None
            os.chdir(os.getcwd())
            os.abort()
            
        except Exception as e:
            self.logger.error(f"Error stopping bot: {e}")
            await update.message.reply_text(f"An error occurred while stopping the bot: {e}")

    @with_typing_action
    @with_log_admin
    @with_register_user
    async def show_user_data(self, update: Update, context: CallbackContext):
        """Show current persistent user data"""
        
        try:
            user_data = context.user_data
            user_data_str = "\n".join(f"{k}: {v}" for k, v in user_data.items())
            await update.message.reply_text(f"Current user data:\n{user_data_str}")
            
        except Exception as e:
            self.logger.error(f"Error showing user data: {e}")
            await update.message.reply_text("An error occurred while showing user data.")
            
    async def post_init(self, app: Application) -> None:
        
        try:
            self.logger.info("Bot post-initialization complete!")
            admin_users = self.config['bot'].get('admin_users', [])
            for admin_id in admin_users:
                try:
                    await app.bot.send_message(chat_id=admin_id, text="Bot post-initialization complete!")
                except Exception as e:
                    self.logger.error(f"Failed to send message to admin {admin_id}: {e}")

            # Set bot commands dynamically
            bot_commands = [
            (f"/{cmd}", handler.description)
            for cmd, handler in self.commands.items()
            ]
            await app.bot.set_my_commands(bot_commands)        

            my_commands = await app.bot.get_my_commands()
            commands_dict = {
            cmd.command: cmd.description or app.bot.commands[cmd.command].__doc__
            for cmd in my_commands
            }

            registered_handlers = [handler.callback.__name__ for handler in app.handlers[0]]

            registered_handlers = [
            f"{handler.callback.__name__}: {', '.join(handler.commands)}"
            for handler in app.handlers[0] if hasattr(handler, 'commands')
            ]

            for handler in app.handlers[0]:
                if hasattr(handler, 'commands'):
                    docstring = handler.callback.__doc__.split('\n')[0] if handler.callback.__doc__ else "No docstring available"
                    self.registered_handlers[', '.join(handler.commands)] = {
                    'handler': handler.callback.__name__,
                    'command': ', '.join(handler.commands),
                    'docstring': docstring
                    }

            self.logger.info(f"Registered handlers: {registered_handlers}")
            
        except Exception as e:
            self.logger.error(f"Error during post-initialization: {e}")

    def run(self, external_handlers:list) -> None:
        app = Application.builder().token(self.token).build()

        async def get_bot_username():
            bot = await app.bot.get_me()
            return bot.username

        # bot_username = app.run(get_bot_username())
        bot_username = 'your_bot_name'
        persistence = PicklePersistence(filepath=f'{bot_username}_bot_data', update_interval=5)

        app = Application.builder().token(self.token).persistence(persistence).post_init(post_init=self.post_init).build()

        # Register command handlers
        for cmd_name in self.commands:
            app.add_handler(TelegramCommandHandler(cmd_name, self.handle_command))

        # Register the list_commands handler
        app.add_handler(TelegramCommandHandler("list_commands", self.handle_list_commands, filters=filters.User(user_id=self.admin_users)))
        
        # Register the Git command handler
        app.add_handler(TelegramCommandHandler("git", self.cmd_git, filters=filters.User(user_id=self.admin_users)))
        
        # Register the restart command handler
        app.add_handler(TelegramCommandHandler("restart", self.restart_bot, filters=filters.User(user_id=self.admin_users)))
        
        # Register the stop command handler
        app.add_handler(TelegramCommandHandler("stop", self.stop_bot, filters=filters.User(user_id=self.admin_users)))

        # Register the show_user_data handler
        app.add_handler(TelegramCommandHandler("show_user_data", self.show_user_data, filters=filters.User(user_id=self.admin_users)))

        # Register the external handlers
        for handler in external_handlers:
            app.add_handler(TelegramCommandHandler("echo", handler), group=-1)

        self.logger.info("Bot started successfully!")
        
        self.app = app
        
        # Call post_init after initializing the bot
        app.run_polling()