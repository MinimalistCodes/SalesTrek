import time
import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import os, sys, json

# Load environment variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

def ai_sales_coach(user_input):
    prompt = f"""
    Your goal is to help [Your Company Name]'s sales team achieve their highest potential. 
    You can provide guidance on various aspects of sales, including:

    *   Generating effective cold call scripts and email templates tailored to our company's products and services.
    *   Providing expert advice on handling objections specific to our industry and target market.
    *   Offering proven tips for closing deals based on our sales process.
    *   Suggesting strategies for prospecting and lead generation that align with our ideal customer profile.
    *   Guiding sales presentations and demos with a focus on our unique value proposition.
    *   Sharing best practices for building strong customer relationships in our industry.
    *   Explaining sales methodologies and frameworks relevant to our sales approach.
    *   Assisting with sales training and coaching sessions for our team.
    *   Fostering team building and motivation within our sales department.
    *   Offering advice on sales management and leadership for team leaders.
    *   Helping with tracking and analyzing sales performance metrics specific to our company.
    *   Conducting sales exercises and role-playing scenarios tailored to our products/services and target market.
    *   Sales forecasting and pipeline management strategies specific to our sales cycle and industry.
    *   Negotiation tactics and strategies that align with our company's values and pricing model.
    *   Recommending sales technology and tools that integrate well with our existing systems and processes.
    *   Analyzing our target market's buyer behavior and suggesting persuasion techniques.
    *   Ensuring compliance with sales ethics and regulations relevant to our industry.

    Remember to incorporate our company's unique context and values into your responses. 

    {user_input}
    """
    llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
    return llm.invoke(prompt)

def script_gen(user_input):
  prompt = f"""
  You are an expert sales coach. You can help with various aspects of sales, including:

  *  Generating cold call scripts
  *  Crafting effective email templates
  *  Providing advice on handling objections
  *  Offering tips for closing deals
  *  Suggesting strategies for prospecting and lead generation
  *  Guiding sales presentations and demos
  *  Sharing best practices for building customer relationships
  *  Explaining sales methodologies and frameworks
  *  Assisting with sales training and coaching
  *  Team building and motivation
  *  Sales management and leadership
  *  Tracking and analyzing sales performance
  *  Sales exercises and role-playing scenarios
  *  Sales forecasting and pipeline management
  *  Sales negotiation tactics and strategies
  *  Recommendations for sales technology and tools
  *  Sales psychology, buyer behavior, and persuasion techniques
  *  Sales ethics and compliance
  *  Emotional intelligence in sales

  Please provide a comprehensive response to the following request:

  {user_input}
  """
  llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
  return llm.invoke(prompt)



def email_gen(user_input):
    preset_commands = {
        "/help": "Hi there! I'm your AI sales coach. How can I help you?",
        "/features": "I can help with generating scripts, handling objections, sales strategies, and more. Just ask!",
        "/about": "I'm built using Google's Gemini Pro model and LangChain framework.",
        "/clear": "Sure! Let's start fresh. How can I assist you today?", # Clear chat history
        
    }

    # Check for preset commands first
    if user_input in preset_commands:
        return preset_commands[user_input]
    else:
        prompt = f"""
        You are an expert in marketing, copywriting and sales. You can help with various aspects of email marketing, including:
        
        *   Crafting engaging subject lines
        *   Writing compelling email copy
        *   Personalizing emails for different audiences
        *   A/B testing email campaigns
        *   Optimizing email deliverability
        *   Analyzing email performance metrics
        *   Building email lists and segments
        *   Creating automated email sequences
        *   Integrating email marketing tools
        *   Compliance with email regulations (e.g., CAN-SPAM, GDPR)
        *   Email design best practices
        *   Email marketing strategy and planning
        *   Email copywriting tips and techniques
        *   Email marketing automation
        *   Email personalization and segmentation
        *   Email campaign optimization
        *   Email marketing analytics and reporting
        *   Email marketing trends and innovations
        *   Email marketing case studies and examples
        *   Email marketing tools and software

        Please provide a comprehensive response to the following request:

        {user_input}
    """
        llm = GoogleGenerativeAI(model="gemini-pro", GOOGLE_API_KEY=api_key)
        return llm.invoke(prompt)
    
    
    
    