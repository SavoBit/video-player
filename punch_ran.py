import logging
import socket
import netifaces as ni

logger = logging.getLogger()

remote_host="193.136.92.197"
remote_port=9099
resolution="1920-1080"
#resolution="176-144"
#host_if='enp0s25'
host_if='wwp0s29u1u1i3'

session = '''
v=0
o=MP4Streamer 3357474383 1148485440000 IN IP4 {host_ip}
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
a=framesize:96 {resolution}
a=fmtp:96'''



def main(remote_host=remote_host, remote_port=remote_port, resolution=resolution):
    ni.ifaddresses(host_if)
    host_ip = ni.ifaddresses(host_if)[ni.AF_INET][0]['addr']

    sock_rtp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
    sock_rtp.bind((host_ip, 0))
    sock_rtp.sendto(b'batatas', (remote_host, remote_port))
    _, port_rtp = sock_rtp.getsockname()

    sock_rtcp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_rtcp.bind((host_ip, port_rtp+1))
    sock_rtcp.sendto(b'cebolas', (remote_host, remote_port+1))
    _, port_rtcp = sock_rtcp.getsockname()

    print("VIDEO RESOLUTION: " + resolution)
    print("HOST IP: " + host_ip)
    print("HOST RTP PORT: " + str(port_rtp))
    print("HOST RTCP PORT: " + str(port_rtcp))

    with open('./session.sdp','w') as f:
        print(session.format(host_ip=host_ip, host_port=port_rtp, resolution=resolution), file=f)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    main()
