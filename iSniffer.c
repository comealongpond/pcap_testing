#include <stdio.h>
#include <stdlib.h>

#include <pcap.h>


int main(void)
{
	char errbuf[PCAP_ERRBUF_SIZE]; 
	struct pcap_if* DAFLC = NULL; // Devices Available For Live Capture


	//Find all devices available for live capture
	pcap_findalldevs(&DAFLC, errbuf);


	//Print all devices available for live capture
	printf("Devices Available For Capture: \n");
	int counter = 0;
	struct pcap_if* DAFLC_cpy = DAFLC;
	while(DAFLC_cpy->next != NULL)
	{
		printf("%i: %s\n", counter++, (DAFLC_cpy++)->name);
	}

	
	//Simply choose the first available device, for now...
	const char* captureDevice = DAFLC->name;
	printf("Using Device: %s For Live Capture\n", captureDevice);


	//Create the capturer
	pcap_t* capturer = pcap_create(captureDevice, errbuf);

	//Activate the capturer (Online), 0 = success, < 0 = success with warnings (which I treat as fail), > 0 fail
	if(pcap_activate(capturer) != 0)
	{
		printf("Failed to activate device \'%s\' for capture.\n", captureDevice);
		printf("ERROR: %s\n", pcap_geterr(capturer));
		return -1;
	}
	//else not really needed since return in if, but makes code easier to read
	else printf("Successfully opened device \'%s\' for capturing\n", captureDevice);


	printf("Available datalinks:\n");
	int *dlt_buf;
	int tmp = pcap_list_datalinks(capturer, &dlt_buf);
	int i = 0;
	for(; i++ <= tmp;)printf("%i. %i\n", i, *dlt_buf);


	/******** Works not *******/
	struct pcap_pkthdr* packet_header = (struct pcap_pkthdr*) malloc(sizeof(struct pcap_pkthdr));
	packet_header->caplen = (bpf_u_int32) 1;
	packet_header->len = (bpf_u_int32) 32;
	struct timeval ts;
	ts.tv_sec = 20;
	packet_header->ts = ts;
	const u_char* pkt_data = pcap_next(capturer, packet_header); 
	/***************************/

	printf("Packet Data: %s\n", pkt_data);


	return 0;
}