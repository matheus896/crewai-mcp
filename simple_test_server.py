from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Simple Echo")

@mcp.tool()
# coment: This is a simple echo tool that returns the input text.

def echo(text: str) -> str: return text

if __name__ == "__main__": mcp.run()