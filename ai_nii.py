import logging
from typing import Dict

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, ApplicationBuilder, ContextTypes, CallbackQueryHandler, filters, ConversationHandler, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE, TYPING_BRIEF = range(4)

def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])

reply_keyboard = [
    ["How I work?", "See Our Work"],
    ["Hire A Designer", "Something else..."],
    ["Done"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="..."
    )

    photo_url = "https://i.pinimg.com/736x/b5/2f/a6/b52fa66d3b790de27c8a3d85713607cb.jpg"
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=photo_url,
        caption=""
    )

    await update.message.reply_text(
        "Hi, I am [name] and this is my profile."
        " How may I help you today?",
        reply_markup=markup,
    )

    return CHOOSING

async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["choice"] = text

    if text == "How I work?":
        await update.message.reply_text("Here's how I work, as a creative assistant - my job is to help you identify the kind of work you want done. Additionally, I will then forward your directives to the agency")
    elif text == "See Our Work":
        await show_portfolio(update, context)
    elif text == "Hire A Designer":
        reply_markup = ReplyKeyboardMarkup(
            [["Event Poster", "Illustration", "Brand Identity", "Web Design"]],
            one_time_keyboard=True,
            resize_keyboard=True
        )
        await update.message.reply_text("To Hire A Designer. You Have To Choose The Kind Of Design You Are Looking At:",
                                        reply_markup=reply_markup)
        return TYPING_BRIEF 

    return TYPING_REPLY

async def hire_designer(update, context):
    buttons = [
        [InlineKeyboardButton("Event Poster", callback_data="hire_designer"),
        InlineKeyboardButton("Illustration", callback_data="hire_designer")],
        [InlineKeyboardButton("Brand Identity", callback_data="hire_designer"),
        InlineKeyboardButton("Web Design", callback_data="hire_designer")]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text("To Hire A Designer. You Have To Choose The Kind Of Design You Are Looking At:", reply_markup=reply_markup)

async def show_portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str = None):
    categories = {
        "Brand Identity": [
            "https://i.pinimg.com/736x/cc/42/78/cc4278cacaa9d36e124692725975eb94.jpg",
            "https://i.pinimg.com/736x/8d/2a/22/8d2a22520580e5a3a39462e77a6dedbd.jpg",
            "https://i.pinimg.com/736x/08/b9/2f/08b92fa815cf7fe7170ae29eac6f6d99.jpg",
            "https://i.pinimg.com/736x/32/1d/37/321d372fa4c0eb40deb725f9003fae71.jpg",
            "https://i.pinimg.com/564x/75/cf/8a/75cf8a92c3e00a22830f5b25c93b47a2.jpg",
            "https://i.pinimg.com/564x/6c/c7/65/6cc76538fd23662c2b8fe1bff21752ed.jpg",
            "https://i.pinimg.com/564x/15/68/37/1568371deabf68f75e19f2074a6d46a1.jpg",
            "https://i.pinimg.com/736x/07/0a/4d/070a4dfebf83d36eb19136ea7290238e.jpg",
        ],
        "Event Posters": [
            "https://i.pinimg.com/474x/e7/2e/9d/e72e9d217c5e1aa5a738a35528267453.jpg",
            "https://i.pinimg.com/736x/5e/5a/fc/5e5afc35d6dbf522cbb305322b29a4bc.jpg",
            "https://i.pinimg.com/564x/19/07/69/1907692b4395363413dee58c0c785340.jpg",
            "https://i.pinimg.com/736x/a2/ce/2b/a2ce2b094ce498dbc70ba490191836aa.jpg",
            "https://i.pinimg.com/736x/04/6e/be/046ebe782ce4be2f7eb1c80875f7582b.jpg",
            "https://i.pinimg.com/736x/33/a3/85/33a385cf168a70a1a79b32bcc9aed646.jpg",
        ],
        "Illustrations": [
            "https://i.pinimg.com/564x/41/ee/f5/41eef51bea82b9670c8e69d253e24baa.jpg",
            "https://i.pinimg.com/564x/67/a1/3c/67a13cf926bfab690a113c2d3eac779e.jpg",
            "https://i.pinimg.com/564x/4f/c7/59/4fc759501762eb283c1a8df4c38ae8f1.jpg",
            "https://i.pinimg.com/736x/eb/ac/da/ebacda8d1947224a7e96df4218962a2c.jpg",
            "https://i.pinimg.com/736x/3d/76/de/3d76de2e5fb632755cd9ae0f5d820c8a.jpg",
            "https://i.pinimg.com/736x/d5/3c/21/d53c2150cab8d7e30b75e636fad43df4.jpg",
        ],
    }

    buttons = []
    for category, _ in categories.items():
        buttons.append([InlineKeyboardButton(category, callback_data=f"show_images_{category}")])

    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("Choose a category to view images:", reply_markup=reply_markup)

async def show_images(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    category = query.data.split("_")[-1]
    categories = {
        "Brand Identity": [
            "https://i.pinimg.com/736x/cc/42/78/cc4278cacaa9d36e124692725975eb94.jpg",
            "https://i.pinimg.com/736x/8d/2a/22/8d2a22520580e5a3a39462e77a6dedbd.jpg",
            "https://i.pinimg.com/736x/08/b9/2f/08b92fa815cf7fe7170ae29eac6f6d99.jpg",
            "https://i.pinimg.com/736x/32/1d/37/321d372fa4c0eb40deb725f9003fae71.jpg",
            "https://i.pinimg.com/564x/75/cf/8a/75cf8a92c3e00a22830f5b25c93b47a2.jpg",
            "https://i.pinimg.com/564x/6c/c7/65/6cc76538fd23662c2b8fe1bff21752ed.jpg",
            "https://i.pinimg.com/564x/15/68/37/1568371deabf68f75e19f2074a6d46a1.jpg",
            "https://i.pinimg.com/736x/07/0a/4d/070a4dfebf83d36eb19136ea7290238e.jpg",
        ],
        "Event Posters": [
            "https://i.pinimg.com/474x/e7/2e/9d/e72e9d217c5e1aa5a738a35528267453.jpg",
            "https://i.pinimg.com/736x/5e/5a/fc/5e5afc35d6dbf522cbb305322b29a4bc.jpg",
            "https://i.pinimg.com/564x/19/07/69/1907692b4395363413dee58c0c785340.jpg",
            "https://i.pinimg.com/736x/a2/ce/2b/a2ce2b094ce498dbc70ba490191836aa.jpg",
            "https://i.pinimg.com/736x/04/6e/be/046ebe782ce4be2f7eb1c80875f7582b.jpg",
            "https://i.pinimg.com/736x/33/a3/85/33a385cf168a70a1a79b32bcc9aed646.jpg",
        ],
        "Illustrations": [
            "https://i.pinimg.com/564x/41/ee/f5/41eef51bea82b9670c8e69d253e24baa.jpg",
            "https://i.pinimg.com/564x/67/a1/3c/67a13cf926bfab690a113c2d3eac779e.jpg",
            "https://i.pinimg.com/564x/4f/c7/59/4fc759501762eb283c1a8df4c38ae8f1.jpg",
            "https://i.pinimg.com/736x/eb/ac/da/ebacda8d1947224a7e96df4218962a2c.jpg",
            "https://i.pinimg.com/736x/3d/76/de/3d76de2e5fb632755cd9ae0f5d820c8a.jpg",
            "https://i.pinimg.com/736x/d5/3c/21/d53c2150cab8d7e30b75e636fad43df4.jpg",
        ],
    }

    media_list = [InputMediaPhoto(media=image) for image in categories[category]]
    await context.bot.send_media_group(chat_id=query.message.chat_id, media=media_list)

    buttons = [
        [InlineKeyboardButton("Something else", callback_data="something_else")],
        [InlineKeyboardButton("That's all", callback_data="done")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.reply_text("Do you want to see more images or are you done?", reply_markup=reply_markup)


async def something_else(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Get the options that were not selected from "See Our Work" and excluding "Brand Identity"
    remaining_options = ["How I work?", "Hire A Designer", "Done"]
    if "See Our Work" in context.user_data.get("choice", []):
        remaining_options.remove("See Our Work")
    if "Brand Identity" in context.user_data.get("choice", []):
        remaining_options.extend(["Event Posters", "Illustrations"])

    context.user_data.pop("choice", None)

    # this will resend the message with the remaining options
    markup = ReplyKeyboardMarkup([remaining_options], one_time_keyboard=True)
    await query.message.reply_text(
        "Now, choose from the below options",
        reply_markup=markup,
    )

async def custom_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    text = update.message.text
    
    if "brief" in user_data:
        await received_information(update, context)
        return CHOOSING
    else:
        await update.message.reply_text(
            'Alright, please see if it falls under any of the options, for example "See our work, Hire a designer"'
        )
        return TYPING_CHOICE

async def choose_design(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["design_type"] = text

    # Ask the user to provide the design brief
    await update.message.reply_text("Please write your design brief.")
    return TYPING_BRIEF  

async def received_information(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    text = update.message.text
    category = user_data.get("design_type")
    
    if category:  # If the user selects a design type
        if "brief" not in user_data:
            user_data["brief"] = text
            user_info = facts_to_str(user_data)
            await update.message.reply_text(f"Awesome! Here's what you've provided so far:\n{user_info}\n\nNow please select another option or choose 'Done' to end the conversation.", reply_markup=markup)
            return CHOOSING
        else:
            await update.message.reply_text("You have already provided a brief. Please select another option or choose 'Done'.", reply_markup=markup)
            return CHOOSING
    else:  # If the user has not written a design brief yet
        await update.message.reply_text(
            "Please write a design brief first.",
            reply_markup=markup
        )
        return TYPING_BRIEF 

async def received_information_text(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Awesome!")
    return CHOOSING  

async def received_information_choice(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Awesome!")
    return CHOOSING 

async def received_information_brief(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    
    # if the design brief has all the keywords
    if is_design_brief(text):
        await update.message.reply_text("Thank you for providing the design brief!")
        return CHOOSING  
    else:
        # if the brief does not have all the keywords
        await update.message.reply_text("Please provide a complete design brief. Make sure the brief has the following keywords: Project title,Project description, Design requirement, Creative brief, Deadline and Additional notes ")
        return TYPING_BRIEF  # send back to write brief again

def is_design_brief(text: str) -> bool:
    # these are the brief keywords
    design_keywords = ["project title", "project description", "design requirements", "creative brief", "deadline", "website redesign", "poster design", "illustration project", "brand identity", "web design"]
    
    missing_keywords = [keyword for keyword in design_keywords if keyword.lower() not in text.lower()]
    
    # If any keyword is missing, it will return False
    if missing_keywords:
        return False
    
    # If all keywords are found, it will return True
    return True


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    user_info = facts_to_str(user_data)
    user_id_to_send_info_to = 5758927976  # Always remember to insert userId here 
    user_to_send_info_to = await context.bot.get_user(user_id_to_send_info_to)
    await user_to_send_info_to.send_message(f"User info: {user_info}")
    await update.message.reply_text("Your information has been sent to the agency.")

    user_data.clear()
    return ConversationHandler.END


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

if __name__ == '__main__':
    TOKEN = 'insert token here'

    application = ApplicationBuilder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex("^(How I work\?|See Our Work|Hire A Designer)$"), regular_choice
                ),
                MessageHandler(filters.Regex("^Something else...$"), custom_choice),
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                    received_information,
                )
            ],
            TYPING_BRIEF: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), received_information_brief),
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), received_information_text),
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), received_information_choice)
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('caps', caps))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    application.add_handler(CommandHandler('hire_designer', hire_designer))
    application.add_handler(CallbackQueryHandler(show_images, pattern=r"^show_images_"))

    application.run_polling()
