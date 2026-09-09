import ipaddress,os
from django.http import HttpResponseForbidden
class InstitutionalNetworkMiddleware:
 def __init__(self,get_response): self.get_response=get_response; self.networks=[ipaddress.ip_network(x.strip()) for x in os.getenv("ALLOWED_ADMIN_NETWORKS","127.0.0.1/32").split(",") if x.strip()]
 def __call__(self,request):
  if request.path.startswith("/admin/"):
   try: ip=ipaddress.ip_address(request.META.get("REMOTE_ADDR",""))
   except ValueError: return HttpResponseForbidden("Acesso administrativo permitido somente pela rede institucional/VPN.")
   if not any(ip in n for n in self.networks): return HttpResponseForbidden("Acesso administrativo permitido somente pela rede institucional/VPN.")
  return self.get_response(request)
