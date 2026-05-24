START_BYTE = 0x7E
END_BYTE = 0x7F

TYPE_DATA = 1
TYPE_ACK = 2

buffer = bytearray()

def calculate_checksum(data):
    return sum(data) % 256


def create_packet(seq, packet_type, payload):

    payload_bytes = payload.encode()
    length = len(payload_bytes)
    packet = bytearray()
    packet.append(START_BYTE)
    packet.append(seq)
    packet.append(packet_type)
    packet.append(length)
    packet.extend(payload_bytes)
    checksum = calculate_checksum(packet[1:])

    packet.append(checksum)
    packet.append(END_BYTE)

    return bytes(packet)


def input_bytes(data):

    global buffer

    # Add incoming data
    buffer.extend(data)

    packets = []

    while True:

        # Find START byte
        if START_BYTE not in buffer:
            buffer.clear()
            break

        start_index = buffer.index(START_BYTE)

        # Remove garbage before START
        if start_index > 0:
            del buffer[:start_index]

        # Minimum packet size check
        if len(buffer) < 6:
            break

        seq = buffer[1]
        packet_type = buffer[2]
        length = buffer[3]

        total_size = length + 6  

        # Wait for complete packet
        if len(buffer) < total_size:
            break

        packet = buffer[:total_size]

        # Verify END byte
        if packet[-1] != END_BYTE:

            print("Invalid END byte")

            del buffer[0]
            continue

        payload = packet[4:4+length]

        received_checksum = packet[-2]

        calculated_checksum = calculate_checksum(packet[1:-2])

        # Verify checksum
        if received_checksum != calculated_checksum:

            print("Corrupted packet discarded")

            del buffer[:total_size]
            continue

        # Store valid packet
        packets.append({
            "seq": seq,
            "type": packet_type,
            "payload": payload.decode(errors="ignore")
        })

        # Remove processed packet
        del buffer[:total_size]

    return packets






import time

received_sequences = set()

waiting_ack = {}

ACK_TIMEOUT = 2
MAX_RETRIES = 5

def create_ack(seq):

    return create_packet(seq, TYPE_ACK, "")

def send_reliable(seq, payload):

    packet = create_packet(seq, TYPE_DATA, payload)

    waiting_ack[seq] = {
        "packet": packet,
        "time": time.time(),
        "retries": 0
    }

    print("SEND:", packet)

    return packet

def process_ack(seq):

    if seq in waiting_ack:

        del waiting_ack[seq]

        print("ACK RECEIVED:", seq)

#time handling
def check_timeouts():

    current_time = time.time()

    resend_packets = []

    for seq in waiting_ack:

        packet_info = waiting_ack[seq]

        # Check timeout
        if current_time - packet_info["time"] > ACK_TIMEOUT:

            # Too many retries
            if packet_info["retries"] == MAX_RETRIES:

                print("FAILED:", seq)

            else:

                # Increase retry count
                packet_info["retries"] += 1

                # Update resend time
                packet_info["time"] = current_time

                # Add packet for resend
                resend_packets.append(packet_info["packet"])

                print("RESEND:", seq)

    return resend_packets


def process_packet(packet):

    seq = packet["seq"]

    if packet["type"] == TYPE_ACK:

        process_ack(seq)

        return []

    if packet["type"] == TYPE_DATA":

        # Duplicate detection
        if seq in received_sequences:

            print("DUPLICATE IGNORED:", seq)

            ack = create_ack(seq)

            return [ack]

        received_sequences.add(seq)

        print("MESSAGE RECEIVED:", packet["payload"])

        ack = create_ack(seq)

        return [ack]

    return []



