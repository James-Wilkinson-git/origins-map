#!/usr/bin/env python3
"""One-off: write data/exhibitors-hall.tsv from bundled rows."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "exhibitors-hall.tsv"

ROWS = r"""
25th Century Games	1808	25thcenturygames.com
9th Level Games	2101	9thlevel.com
Academy Games	2401	academygames.com
Adventurers' Stationery & Supply Co	2109	instagram.com/adventurersstationery
Aeonian Dawn	14200	aeoniandawn.com
After Sunfall	1717	aftersunfall-dusk.carrd.co
Alchemy Art	1515	
Allplay	1206	allplay.com
Allplay	1208	allplay.com
Alpha Clash	2207	alphaclashtcg.com
Alternate Universes	1918	alternateu.company.site/products
Ancient Innovations	2020	ancient-innovations.com
Andrew Heath Design + Illustration	1518	andrew-heath.com
Andy Kehoe Art	2406	andykehoe.art
Arcadian Chain	2214	arcadianchain.com
Arcane Wonders	1022	arcanewonders.com
Archania's Workshop, LLC	1212	archaniaworkshop.com
Archon Games	1907	archongames.net
Area of Effect Rugs	1606	areaofeffectrugs.com
Around The Stump Games	2307	outrunthebeargame.com
Art by Charles Urbach	15010	etsy.com/shop/CharlesUrbachArt
Art of David Wong	1525	artofdavidwong.com
Art of Jessy	14140	artofjessy.com
Art of Kellianne Stakenas	1216	patreon.com/DrawingSpiffily
Artistic Realms	1524	christinemarchi.com
ArtisXan	2111	artisxan1.myshopify.com
Arty Alex Creations	1325	artyalexcreations.com
Ashyfeet Games	1610	ashyfeet.com
Asmodee	2218	asmodeena.com
Author Ray Wenck	1517	raywenck.com
B.A. Games	2009	bagamesco.com
Band of Idiots	2807	bandofidiots.store
Bard & Broad	1710	bardandbroad.com
beldolor Studios	1104	beldolorstudios.com
Best Man Gaming LLC (Flawed TCG)	2702	flawedcardgame.square.site
Bezier Games, Inc	1320	beziergames.com
BigCritCrew Investments	2012	bigcritcrew.com
Biosymfonix Game Knights	1302	pactopolis.com
Bitewing Games	1906	bitewinggames.com
Black Labrador Creations, LLC	1018	blacklabradorcreations.com
Black Oak Workshop	1203	blackoakworkshop.com
Black Oak Outpost	2708	blackoakworkshop.com
BlindCoyote	2017	blindcoyote.com
BLUE ORANGE GAMES	1902	blueorangegames.com
Blue Rondo Games	2617	bluerondogames.com
Boda Games Manufacturing	1306	bodagames.com
Boiling Point Games	1713	boilingpointgames.com
Book Loft of German Village	2706	bookloft.com
Brave Legacy Games	1406	bravelegacy-games.com
Breakout Columbus	1724	breakoutgames.com/columbus
Broken Blade Publishing	2103	thebrokenblade.com
Brown Castle Games	2811	browncastlegames.com
Capstone Games	1311	capstone-games.com
Captive Fancy	2010	Captive-fancy.square.site
Castle Keep Crafts	1915	facebook.com/Castlekeepcrafts
Catawampus Press	1315	catawampuspress.com
CavernHold	2313	cavernhold.com
CB3's Studio & Gaming	1014	cb3studios.com
Chaosium	2402	chaosium.com
Chess Up	1107	playchessup.com
Chicken Challengers	1504	chickenchallengers.com
Chooseco (Choose Your Own Adventure)	2108	cyoa.com
Chris Couch Games	1714	chriscouch.games
Citrus Atelier	1621	instagram.com/citrusatelier
Cleromancy Games LLC	2512	wornwanderers.com
Cleverland Puzzle	1624	cleverlandpuzzle.com
Collectible Empire, LLC	2014	youtube.com/shorts/zryRfSM
Collector's Cache	2709	collectorscache.com
Combee Collectibles	1313	combeecollectibles.com
Comfort Kingdom	15020	comfort-kingdom.com
Constellation Collective Sacramento LLC	2809	constellationcollectivesac.com
CoolStuffinc	2317	
Cosplay Deviants	2500	cosplaydeviants.shop
Crates of Chaos	2806	cratesofchaos.com
Creature Curation/Vast Grim	2100	creaturecuration.com
Cribbagio	2210	cribbagio.com
CRIME NO CRIME	1321	crimenocrime.com
Crit Hit Ceramics	2008	crithitceramics.com
Critical Crafting	2201	critical-crafting.com
Cryptid Dicecraft	1626	cryptiddicecraft.com
Crystal Caste	2104	crystalcaste.com
Cube Woodworking	2309	cubewoodworking.com
Cyber Hex	1316	stevemessenger.art
Cyber Wizard Games	2007	cyberwizardgames.com
Czech Games Edition, Inc.	1903	czechgames.com
Dan English, Artist & Illustrator	2213	danenglish.art
Dandyline Games, Super Savage Systems, and Silver Bulette Publishing	1801	super-savage-systems.myshopify.com
Daria Aksenova	1520	dariaaksenova.com
DaSueDragon Designs	2102	dasuedragondesigns.com
DeathDuck	1527	deathduck.com
Decision Games/Strategy & Tactics Press	2705	decisiongames.com
Decus Workshop	2618	decusworkshop.com
Diamond K Games	2513	diamondkgames.com
Dice Dungeons	2212	dicedungeons.com
Dirty Woods	1500	dirtywoods.net
Don Higgins Illustration	1719	donhigginsillustration.com
DPH Games Inc.	1019	DPHGames.com
Dragon Armor Games	1815	dragonarmorgames.com
Dragonfire Press	2609	richardfierce.com
Dragonsworn	1103	dragonsworn.net
Dream Vale Studios	1608	dreamvalestudios.com
Druids Garden Tea Company	2029	druidsgardenteacompany.com
DVC Games	1812	dvc.games
EASTAR	1821	eastarboardgame.com
Eerie Games	2404	eeriegames.com
Egghead Comics and Games	1630	
Enterprise Games	1702	enterprisegames.com
Envy Born Games	2202	envyborngames.com
Epic Armoury	2114	us.epicarmoury.com
Epic Strategic Simulations / VR-Soft	2810	vr-soft.com
Eric Fortune	1418	
Escape Mail	2409	theescapemail.com
Escapely	1509	escapely.com/escape
Evil Genius Games	2302	evilgeniusgames.com
Excelsior	1102	excelsiorpowered.com
ExtraLife	2220	
Fanroll by Metallic Dice Games	2003	fanrolldice.com
Fireside Games	1317	firesidegames.com
First Fish Games	1706	firstfishgames.com
Floral Frolic	2502	floralfrolic.com
Flying Cloud	1816	
Foam Brain Games	1614	foambrain.com
Four Horsemen Studios	1106	sourcehorsemen.com
Fox and Boar Games	2604	facebook.com/foxandboargames
Foxdragon Publishing by Naomi VanDoren Studio	1326	foxdragon.com
FoxHen Creatives	2107	foxhencreatives.com
Foxweave Studios	2510	foxweave.com
Free League Publishing	2603	freeleaguepublishing.com
Friar's Dice	1503	friarsdice.com
FTZ Games	1220	rocknrollbrouhaha.com
Fusion Theory Games	1303	
Game Design	1529	
Game Universe	1820	
Gamehead	1908	gamehead.com
Gameland	1420	gamelandcn.com
Gamer Girl Jewelry	2018	gamergirljewelry.com
Gate Keeper Games & Dice	2403	gatekeepergaming.com
Gaymers Cruise	1632	
Geeky Endeavors	2209	geekyendeavors.com
Genius Games / Elf Creek Games	2511	elfcreekgames.com
GL HF Games	1219	gl-hf-games.com
Goliath Coins	2208	goliathcoins.com
Goodman Games	1807	goodman-games.com
Goosepoop Games	1631	goosepoopgames.com
Grand Gamers Guild	2607	grandgamersguild.com
Grandpa Beck's Games	2002	grandpabecksgames.com
Grex Airbrush	1015	grexusa.com/grexairbrush
Grey Fox Games	1603	greyfoxgames.com
Grimdark Ohio	1211	instagram.com/grimdark.ohio
GrimStylesArt	1912	grimstylesart.com
Handmade Dice by The Griffon's Nest	1721	thegriffonsnest.com
Hearth and Token	1618	hearthandtoken.com
Heartleaf Games	1221	thedelversguide.com
Heavy Play	13060	heavyplay.com
Hectic Electron Games	1813	hecticelectron.com
Hero's Hearth Games	1633	cincybookrack.com
Hillary's Toy Box	1507	hillarystoybox.com
Hrothgar's Hoard	1300	hrothgars-hoard.com
Hymgho Premium GamingSupplies	1919	hymgho.us
Ian Moss Creative	1914	ianmosscreative.com
In My Parents Basement	1001	
Indie GameStudios/Stronghold Games	1301	strongholdgames.com
Indie Press Revolution	1803	
Ink Splot Games	1905	presentsrequested.com
Inside Up Games	2303	insideupgames.com
Inspired Artistry	1628	facebook.com/people/Inspired-Artistry/100035399664478
Interstellar Dice	1622	
Intrepid Gremlin Games	1508	
Ivory Elk Designs	1319	ivoryelkdesigns.com
Jacob Walker Art	2610	
Jamon Red, LLC - Hector Ceniceros III	1421	
Jank Mats	1101	
Japanime Games	2801	japanimegames.com
Joking Hazard	2028	
Justine Dillenbeck Illustrations	15270	
KamoriaArt	1911	kamoriaart.carrd.co
Kawaii Lab Games	2506	kawaiilabgames.com
Kinson Key Games	1620	kinsonkeygames.com
Krit Dice	1720	kritdice.com
Krystaline Studio	1008	
Lacorsa Grand Prix Game	1602	
Last Night Games	2601	lastnightgames.com
Lets Bug Out	1708	
Level UpSabers	2514	
Libib	1505	libib.com
Lilystrations	1417	
Limithron LLC	2300	limithron.com
Limitless Adventures	22110	
Lioness Games	2605	lionessgames.com
Littlest Lantern	1304	littlestlantern.com
LongPack Games & Toys	1528	
Lor Illustration	2112	
Lore Link	2004	lorelink.com
Ludoliminal	1404	ludoliminal.com
Luminous Games	1711	
Lurker's Loot	2703	lurkingfears.com
LUZ-ART	1416	
Mad Dragon Woodcraft	1425	
Magic Minis and More	2800	ebay.com/str/magicminisandmore
Maliveth	1715	maliveth.com
Mantic Games	1016	manticgames.com
MB Kraft Studio	1909	mbkraftstudio.etsy.com
Meeples At Sea	1917	gameconhq.com
Mega Kawaii Cuties	2311	
Merlin's Munchies Coffee Company	1402	merlinsmunchiescoffee.com
Midnight Games	13150	midnightgamesshop.wixsite.com/mysite
Midwest Cards	2316	midwestcards.com
Mighty Pie Creative Workshop	1521	mightypieworkshop.com
Miniature Market	1210	miniaturemarket.com
Mischief Loot	1002	mischiefloot.com
MK Woodcrafts	1011	etsy.com/shop/mkwoodcrafts.com
Moon Crab Games	2613	
MoonSaga Workshop	1516	
moreblueberries	2501	moreblueberries.shop
Moss Fete	2024	moss-fete.com
My Little Demon	1519	
MyNerdLife	2803	mynerdlife.com
Mystic Tomes & Treasures	1201	arcane-ink.com
Mythworks	1423	
Najarian Art	2314	
Nate Lovett	1215	nate-lovett.com
Neuroscape	2701	neuroscapetcg.com
Next Level Miniatures	1010	nextlevelminiatures.com
Nick Jizba	2315	
Nomadic Lasers	2602	linktr.ee/nomadiclasers
Norse Foundry	2205	
Offcut Games	1811	
Offshoots	1607	offshootsgame.com
Origins 2026 Merch	1023	
OUTSET	2611	outsetmedia.com
PACIFIC MIDWEST CREATIONS	2110	facebook.com/pacificmidwestcreations
Pages of Ivy	2015	pagesofivy.co
Paige the Gnome	2216	
Painted Dragon Studios	1213	
Parakeet Griffin Games	1318	parakeetgriffingames.com
Part Time Dragons	2026	parttimedragons.com
Pawley Studios	1314	pawleystudios.com
Pegasus Publishing	1514	pegasuspublishing.com
Piece Keepers	1712	
pineapplebread	1414	
Pink Bunny Games	1819	
Pink Hawk Games	1404	pinkhawkgames.com
Pizza With a Fork LLC	2206	pizzawithaforkgames.com
Placeholder Games	1705	placeholder-games.com
Play to Z	2006	playtozgames.com
PocketParks	2505	pocketparks.com
Pollia Design	1415	polliadesign.com
Portreii	2405	
PostCurious	1806	getpostcurious.com
Potion Dice Emporium	1625	
Pour Over Gaming	1718	pourovergaming.com
Prime Chaos GlassStudios	1722	
Probably Illegal People	1400	
Proper Play Games	1222	
Pushing Tin Games	1020	pushingtingames.com
Quilt Beginnings	2005	quiltbeginnings.com
R. Talsorian	2301	
Race to Stupid Games	1021	racetostupid.com
Restoration Games	1209	resurrection.games
Resurrection Games	2105	
Retro Plus Games	1312	
Rising Empire Studios	1810	
Robin's Nerd Supplies	1601	robinsnerdsupplies.com
Rock Manor Games	1202	rockmanorgames.com
Rockport Games	1403	rockportgames.com
Role 4 Initiative	1802	
Roll With Adventure	2016	
Rose Micro Solutions	1004	
Rose Micro Solutions	2013	
Sage Stones	2704	sagestonesgame.com
Saving Throw Pillows	2023	savingthrowpillows.com
Sea Cow Games	13030	seacowboardgames.com
Sea Dog Games Studios	1017	
SFR Inc	1405	dragondice.com
Shard Bugs	2503	shardbugstcg.com
Silverwood Wood Designs	1809	
Simeous Business	1506	simeousbusiness.com
Sky Kingdom Games	1501	skykingdomgames.com
Sleeping Giant Gaming	1006	sleepinggiantgaming.com
SMASHCRAFT	1217	
Smirk & Dagger Games	2308	smirkanddagger.com
Snowbright Studio	2211	
Sophisticated Cerberus Games	1308	sophisticatedcerberus.com
Soul Masters TCG	2318	
Speedrobo Games/TCG Co	1200	speedrobogames.com
SRG Universe	1214	
STACCS	2306	sticcy.cc
Steampunk Garage - Chainmaille	2027	steampunkgarage.com
Stitchology Crafts	2608	stitchologycrafts.com
Stone Age Entertainment	1814	stoneageentertainment.com
Story Garden Publishing	1818	jordanrileyswan@gmail.com
Strange Machine Games	1422	
Studio 2 Publishing	1307	studio2publishing.com
Studio de Sade: Fine Art of Nigel Sade	1526	
Studio Pen Pen	1522	
Studio Smithy Art	1817	
Studio Woe	1012	
Sugarbplays DIY CrossStitch	1913	
Surfin' Meeple	2219	
Tabletop Gaymers	1000	tabletopgaymers.org
Taco Cat Games (Dolphin Hat Games)	2305	tacocatgames.com
Tangled Earth Arts	2312	facebook.com/tangledeartharts
Tea And Absinthe/Alchemist's Dust	2025	
Teakettler Games	1424	
Teaweltzer	1623	teaweltzer.carrd.co
Tee Turtle / Unstable Games	2509	
TeeMinus24.com	14030	teeminus24.com
Terrible Games	1531	tokenterrors.com
Terry Huddleston ART	2805	
The Arcane Threadery	1218	
The Army Painter	1013	thearmypainter.com
The Art of Brent Chumley	2021	brentchumley.com
The Art of Jeremy Provost	1916	
The Art of Michael C. Hayes	1619	artofmike.com
The Bodhana Group	1502	thebodhanagroup.org
The Dice Goblin	1707	thedicegoblinus.com
The Dicey Dungeon	2022	
The Flickering Lantern	2113	theflickeringlantern.store
The Game Steward	1309	
The Geek Preacher	2515	
The Gilded Teafling	2408	
The Merchant of Many Things	2508	themerchantofmanythings.myshopify.com
The Soldiery Games & Cards	2615	thesoldiery.com
Thor Custom Designs	2217	
Toth Games	1617	tothgames.com
Tournament of Pieces	2710	
Triforge Laser Design	2215	
Trivium Studios	2001	triviumstudios.com
TTCombat	1205	ttcombat.com
TUBBZ	1005	tubbzus.com
Tuesday Knight Games	1604	tuesdayknightgames.com
Tulipitful	1310	
Twin Tale Studios	2707	twintalestudios.com
Uloomi	2507	
Under the Covers	1419	
Upended Games	1605	
Vala Foundry	1204	
Van Ryder Games	2203	
Vesuvius Media	1322	vesuviusmedia.com
Wabi Blobi	1612	wabiblobi.com
Warlord Games	2808	
Waterbear Workshop	1611	waterbearworkshop.com
Wattsalpoag Games	1401	wattsalpoag.myshopify.com
We Ride Games	1530	
Weathervane Games	2612	
Weighted Dice Games	1805	weighteddicegames.com
Weird Place	1609	weirdplace.net
Welcome Home CreationsTn	2606	welcomehomecreationstn.com
Wet Ink Games	1901	
Whales Entertainment	1723	
Wherever Games	16050	kotamconquest.com
Wild Bill's Soda	2115	
Wired Dice Goblin	1523	Wired-dice-goblin.square.site
Witches' Quarrel	2504	
WizKids	2802	
Wyvern Warfare	1910	
XP Network	1904	
XP Network Outpost	2011	
ZenJumps Chainmaille	1627	zenjumpschainmaille.com
Zero Strategy Games	1704	zerostratgames.com
""".strip()

def main() -> None:
    OUT.write_text(
        "Exhibiting As Name\tBooth Number\tWebsite\n" + ROWS + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUT} ({len(ROWS.splitlines())} rows)")


if __name__ == "__main__":
    main()
