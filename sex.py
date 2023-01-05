import requests
import os
import discord

r = requests.head(url="https://discord.com/api/v1%22")
print(r.headers)
try:
    print(f"Rate limit {int(r.headers['Retry-After']) / 60} minutes left")
except:
    print("No rate limit")