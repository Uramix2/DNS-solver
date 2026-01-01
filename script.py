import dns.resolver
import sys

liste = [
    "A",
    "AAAA",
    "MX",
    "NS",
    "TXT",
    "SOA",
    "CNAME",
    "CAA",
    "PTR",
    "SRV",
    "NAPTR",
    "DNSKEY",
    "DS",
    "RRSIG",
    "NSEC",
]
def dns_type(domain, liste):
    """
    Permet d'afficher les types de dns via brute force
    """
    resolver = dns.resolver.Resolver()
    result = {}
    for e in liste:
        try:
            answers = resolver.resolve(domain, e)
            values = [str(r) for r in answers]
            if values:
                result[e] = values
        except Exception as ex:
            print(e, "error : -->", type(ex).__name__)
            continue
    return result



imput = sys.argv[1]
print(dns_type(imput,liste))





            

    





