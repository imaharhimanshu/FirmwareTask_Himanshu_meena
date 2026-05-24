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

 SEQUENCE NUMBER= Used to maintain order of packets (0, 1, 2...).
                      Helps detect duplicate or missing packets.

 LENGTH= Indicates the size of the message (payload).


 PAYLOAD (MESSAGE)=  The actual data being sent .

 CHECKSUM=If data is corrupted during transmission, checksum will not match and packet is rejected.

CRC= it helps to detect corruption . if received_crc = calculated_crc  then no error in data otherwise some mistaken happened.

CREAT-PACKET =it construct a complete communication packet by converting the payloads in bytes and also add start,type,seq,length.

input_bytes(data) =   This functions receive data in bytes then it convert them into packets
	how this works. it add new incoming bytes into  buffer.   if the starting bytes exist then this move further otherwise delete garbage data .
then search for starting byte index from received data. then remove the garbage value before the starting index.
then it checks remaining bytes length if the length lesser than 6 . then we apply breat so this wait for more data. now this read the header values . and then extract payload data . and then check checksum.if received checksum == calculated checksum then fill the data in packet otherwise the data is corrected.

Acknowledgement system =  in the process of communication  when one device sent data to another device . the receiver device sent a acknowledgment if he received the data otherwise it doesn’t send anything . there is some time limit for waiting of acknowledgment .if the acknowleedgment don’t come before the time limit device again send the data there is another parameter tries which track tha5t how many times the device try to sent data. Maximum number of resend attempts. before packet is considered failed.
Stores:   packet bytes  , current send time  ,retry counter

Overall process -  
1 Sender sends data packet

 2. Packet stored in waiting_ack

 3. Receiver receives packet

 4. Receiver sends ACK packet

 5. Sender receives ACK

 6. Sender removes packet from waiting_ack

 7. If acknowledgment not received within timeout:
 packet is resent automatically

 8. Duplicate packets are ignored safely
