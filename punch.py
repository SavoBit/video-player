import logging
import socket
logger = logging.getLogger()

remote_host="193.136.92.197"
remote_port=9099

session = '''
v=0
o=MP4Streamer 3357474383 1148485440000 IN IP4 193.136.92.197
s=livesession
i=This is an MP4 time-sliced Streaming demo
u=http://gpac.sourceforge.net
e=admin@
c=IN IP4 {host_ip}
t=0 0
a=x-copyright: Streamed with GPAC (C)2000-200X - http://gpac.sourceforge.net
m=video {host_port} RTP/AVP 96
a=rtpmap:96 H265/90000
a=mpeg4-esid:1
a=framesize:96 1920-1080
a=fmtp:96'''


def main(remote_host=remote_host, remote_port=remote_port):
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.sendto(b'batatas', (remote_host,remote_port))
    host, port = sock.getsockname()

    with open('./session.sdp','w') as f:
    	print(session.format(host_ip=host, host_port=port), file=f)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    main()
