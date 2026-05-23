# FirmwareTask_Himanshu_meena

1. THE PACKET 

data is packed into a structured format called a packet.
Packet format:  start - type-number-length-message-checksum

 START BYTE:
  A special signal that marks the beginning of a packet.
  It helps the receiver identify where the message starts.

 TYPE:
  Indicates the type of packet:
  1 = Data packet (normal message)
  2 = ACK packet (acknowledgment)

 SEQUENCE NUMBER---- Used to maintain order of packets (0, 1, 2...).
                      Helps detect duplicate or missing packets.

 LENGTH------  Indicates the size of the message (payload).


 PAYLOAD (MESSAGE)-----  The actual data being sent .

 CHECKSUM----If data is corrupted during transmission, checksum will not match and packet is rejected.

CRC ----- it helps to detect corruption . if received_crc = calculated_crc  then no error in data otherwise some mistaken happened.

CREAT-PACKET --- it construct a complete communication packet by converting the payloads in bytes and also add start,type,seq,length.

PARSER ----  it used like Incoming data ->save in buffer ->find START ->check size ->extract packet → verify CRC → if OK → return packet if BAD -> skip byte

DEVICE ---- Each Device is like a smart communication unit that can:
      Sender side: Send packets, Remember last packet sent, Wait for ACK ,Retry if needed (future logic)
      Receiver side: Receive stream of bytes, Parse packets using Packet Parser, Check sequence order, Avoid duplicates / missing packets

receive_data---- TAKES INCOMING BYTES -> convert them to valid packet using parser. then process each packet.

ACK PACKET--- this is like a confirmation message.

RETRANSMISSION CHECK----- in real communication system packets can be lost . ack can be lost, and some other issue can happen so if no response within X seconds then resend message. 
