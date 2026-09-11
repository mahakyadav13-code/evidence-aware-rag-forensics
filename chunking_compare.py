from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter

sample_text = """
On the night of March 5th, the suspect John Doe called Mike Smith at 10:30 PM.
Phone records show the call lasted 14 minutes. Shortly after, at 10:52 PM,
a file named 'transfer.zip' was created on John's laptop. Network logs show
the IP address 192.168.1.5 uploaded this file to an external server at 11:05 PM.
Mike's phone pinged near the old warehouse at 11:15 PM, suggesting he traveled
there shortly after the call ended. Security camera footage near the warehouse
recorded a vehicle matching Mike's car at 11:20 PM.
"""

# Strategy 1: Fixed-size chunking
fixed_splitter = CharacterTextSplitter(chunk_size=150, chunk_overlap=0, separator=" ")
fixed_chunks = fixed_splitter.split_text(sample_text)

# Strategy 2: Recursive chunking with overlap
recursive_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=30)
recursive_chunks = recursive_splitter.split_text(sample_text)

print("=== FIXED-SIZE CHUNKS ===")
for i, c in enumerate(fixed_chunks):
    print(f"[{i}] {c}\n")

print("=== RECURSIVE CHUNKS (with overlap) ===")
for i, c in enumerate(recursive_chunks):
    print(f"[{i}] {c}\n")