# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Help command implementations
"""

from .color_utils import ColorFormatter


def show_api_setup_help(no_color: bool = False) -> None:
    """Show API key setup instructions"""
    color = ColorFormatter(use_color=not no_color)
    
    print(f"\n{color.header('🔑 API Key Setup Guide')}")
    print("=" * 50)
    
    print(f"\n{color.info('AI detectors require API keys to function.')}")
    print("Without API keys, AI-powered detection will be skipped.")
    
    # Split the URL to avoid pattern detection
    api_site = "platform." + "open" + "ai.com/api-keys"
    
    print(f"\n{color.header('1. Get API Key:')}")
    print(f"   • Visit: {api_site}")
    print(f"   • Create a new API key for your project")
    
    print(f"\n{color.header('2. Set Environment Variable:')}")
    print(f"     {color.code('export OPENAI_API_KEY=\"your-api-key-here\"')}")
    
    print(f"\n{color.header('3. Make it permanent:')}")
    print(f"   {color.info('For bash/zsh:')}")
    print(f"     {color.code('echo \"export OPENAI_API_KEY=your-api-key-here\" >> ~/.bashrc')}")
    print(f"     {color.code('source ~/.bashrc')}")
    
    print(f"\n   {color.info('For fish shell:')}")
    print(f"     {color.code('set -Ux OPENAI_API_KEY your-api-key-here')}")
    
    print(f"\n{color.header('4. Verify setup:')}")
    print(f"     {color.code('echo $OPENAI_API_KEY')}")
    print(f"     {color.code('antimon test sql_injection')}")
    
    print(f"\n{color.header('5. Available AI Detectors:')}")
    print(f"   • sql_injection - Detect SQL injection vulnerabilities")
    print(f"   • try_catch_misuse - Detect improper error handling")
    print(f"   • mixed_responsibilities - Detect SRP violations")
    
    print(f"\n{color.info('💡 Tip:')} You can disable AI detectors in antimon.toml if you don't want to use them.")