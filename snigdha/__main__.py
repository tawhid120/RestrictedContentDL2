import asyncio
import importlib
import gc
import os  # (যোগ করা হয়েছে)
import threading  # (যোগ করা হয়েছে)
from pyrogram import idle
from snigdha.modules import ALL_MODULES
from snigdha.core.mongo.plans_db import check_and_remove_expired_users
from aiojobs import create_scheduler
from app import app  # (যোগ করা হয়েছে) Flask অ্যাপ ইম্পোর্ট করুন

loop = asyncio.get_event_loop()

# (যোগ করা হয়েছে) Flask অ্যাপটি চালানোর জন্য একটি ফাংশন
def run_web_server():
    port = int(os.environ.get("PORT", 8000)) # Render-এর দেওয়া PORT ব্যবহার করুন
    print(f"Starting Flask web server on port {port}...")
    app.run(host="0.0.0.0", port=port)
    
async def schedule_expiry_check():
    scheduler = await create_scheduler()
    while True:
        await scheduler.spawn(check_and_remove_expired_users())
        await asyncio.sleep(60)  # Check every 60 seconds
        gc.collect()  # Explicit garbage collection to free memory

async def restrictdl_boot():
    # Import all modules dynamically
    for module in ALL_MODULES:
        importlib.import_module(f"snigdha.modules.{module}")

    # (যোগ করা হয়েছে) ওয়েব সার্ভারটিকে একটি ব্যাকগ্রাউন্ড থ্রেডে চালু করুন
    print("Starting web server in a background thread...")
    web_thread = threading.Thread(target=run_web_server)
    web_thread.daemon = True  # নিশ্চিত করুন যে মূল প্রোগ্রামটি বন্ধ হলে থ্রেডটিও বন্ধ হবে
    web_thread.start()
    print("Web server is running in the background.")
    
    # Schedule the expiry check task
    asyncio.create_task(schedule_expiry_check())
    
    # Keep the bot running
    await idle()

if __name__ == "__main__":
    loop.run_until_complete(restrictdl_boot())
