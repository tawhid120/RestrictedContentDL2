from pyrogram import Client
from config import LOG_GROUP, OWNER_ID
from snigdha import app

async def log_user_activity(client: Client, message, link: str):
    try:
        user = message.from_user
        
        # ইউজারের তথ্য বের করা
        user_name = f"{user.first_name} {user.last_name or ''}".strip()
        user_id = user.id
        username = f"@{user.username}" if user.username else "No Username"
        profile_link = user.mention
        
        # লিংক থেকে সোর্স চ্যানেল/গ্রুপ বের করার চেষ্টা
        source_info = "Unknown Source"
        
        if 't.me/c/' in link:
            # প্রাইভেট চ্যাট লিংক
            try:
                parts = link.split('/')
                chat_id = int("-100" + parts[-2])
                source_info = f"Private Chat ID: {chat_id}"
                # বট যদি ওই চ্যানেলে থাকে তবে নাম বের করার চেষ্টা করবে
                try:
                    chat_obj = await client.get_chat(chat_id)
                    source_info = f"{chat_obj.title} ({chat_id})"
                except:
                    pass
            except:
                pass
        elif 't.me/' in link:
            # পাবলিক লিংক
            try:
                parts = link.split('/')
                # পাবলিক ইউজারনেম বের করা
                if len(parts) >= 4:
                    public_chat = parts[3]
                    source_info = f"Public: @{public_chat}"
            except:
                pass

        # লগ মেসেজ তৈরি করা
        log_text = (
            f"🚨 **New Link Detected!** 🚨\n\n"
            f"👤 **User:** {profile_link}\n"
            f"🆔 **User ID:** `{user_id}`\n"
            f"📛 **Username:** {username}\n\n"
            f"🔗 **Link:** `{link}`\n"
            f"📂 **Source:** `{source_info}`\n"
            f"📅 **Date:** `{message.date}`"
        )

        # লগ গ্রুপে পাঠানো (সবচেয়ে নিরাপদ উপায়)
        if LOG_GROUP:
            await client.send_message(
                chat_id=LOG_GROUP,
                text=log_text,
                disable_web_page_preview=True
            )
        
        # অথবা আপনি চাইলে সরাসরি OWNER_ID তে পাঠাতে পারেন (নিচের অংশ আনকমেন্ট করতে পারেন)
        # for owner in OWNER_ID:
        #     try:
        #         await client.send_message(owner, log_text, disable_web_page_preview=True)
        #     except:
        #         pass

    except Exception as e:
        print(f"Error logging user activity: {e}")
