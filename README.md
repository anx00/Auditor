# Wi-Fi auditing tool based on low-cost boards

Nowadays, the use of wireless networks is growing exponentially in business environments of all kinds. While it is true that there are a large number of solutions in the field of wireless network auditing for large organizations, the solutions that exist for small businesses are scarce, and this together with the lack of knowledge and experience in Information Technology (IT) of the staff of such organizations, causes that these types of companies are usually at a high level of risk in cybersecurity.
In this context we developed a tool that aims to audit wireless networks in enterprise environments, based on low-cost hardware and requiring only a basic level of IT and cybersecurity knowledge by the user.
The architectural design of the tool is based on a distributed system of low-cost devices that allows monitoring and auditing the wireless environment and displaying the information obtained to the user in an intelligible way.
In the current implementation we use Raspberry Pi 3B+ as low-cost boards, to which we connect external Wi-Fi antennas, which facilitate the capture of network traffic. Subsequently, we process such traffic and the obtained results are displayed to the user via a web interface.
After completing the development of the tool, we have carried out tests, both in a real environment and in a simulated environment, which has allowed us to obtain interesting conclusions about the work done.

Key words: Python, Django, Scapy, Raspberry Pi, Wireless antenna, Wi-Fi, Auditing, Nmap.
