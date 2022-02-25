import os, sys, requests, json
from packaging import version

import consts

apple_gdmf = "https://gdmf.apple.com/v2/pmv"

reqs = requests.Session()

resp = reqs.get(apple_gdmf, verify="gdmf-apple-com-chain.pem")
catalog = resp.json()

if consts.DEBUG: print("-- Current DB --")
for Model in consts.apple_id:
	if consts.DEBUG: print("%s -|- %s" % (Model,len(consts.apple_id[Model])))

if consts.DEBUG: print("")
if consts.DEBUG: print("-- Device Versions --")

for iOS in catalog["PublicAssetSets"]["iOS"]:
	for Device in iOS["SupportedDevices"]:
		for Model in consts.apple_id:
			if Device in consts.apple_id[Model]:
				if consts.DEBUG: print("%s (%s)" % (consts.apple_id[Model][Device], iOS["ProductVersion"]))
				if iOS["ProductVersion"] not in consts.latest_versions[Model]:
					consts.latest_versions[Model].append(iOS["ProductVersion"])
#			else:
#				print("Unknown ID")


for macOS in catalog["PublicAssetSets"]["macOS"]:
	for Device in macOS["SupportedDevices"]:
		for Model in consts.apple_id:
			if Device in consts.apple_id[Model]:
				if consts.DEBUG: print("%s (%s)" % (consts.apple_id[Model][Device], macOS["ProductVersion"]))
				if macOS["ProductVersion"] not in consts.latest_versions[Model]:
					consts.latest_versions[Model].append(macOS["ProductVersion"])
#			else:
#				print("Unknown ID")

if consts.DEBUG: print("")
print("-- Results --")
if consts.DEBUG: print(consts.latest_versions)

for Model in consts.latest_versions:
	lver = "0.0.0"
	for ver in consts.latest_versions[Model]:
		if version.parse(ver) > version.parse(lver): lver = ver
	print("%s | %s" % (Model,lver))

sys.exit(0)	