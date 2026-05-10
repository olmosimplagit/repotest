#!/usr/bin/env python3
import argparse
import random
import time
from concurrent.futures import ThreadPoolExecutor
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

list_of_domains = [
    "jpeg.org",
    "etramping.com",
    "newlinesmag.com",
    "nub.rs",
    "roe.ru",
    "anc.org.za",
    "letsview.com",
    "damemagazine.com",
    "politicalcompass.org",
    "mouseplanet.com",
    "photostockeditor.com",
    "cleverism.com",
    "thoughtleader.co.za",
    "flyroyalbrunei.com",
    "gadnr.org",
    "criticalthinking.org",
    "abidjan.net",
    "mthai.com",
    "tempi.it",
    "hermancain.com",
    "blinknetwork.com",
    "velodynelidar.com",
    "gomerblog.com",
    "teachpsych.org",
    "gitmind.cn",
    "munnari.oz.au",
    "soroban.ua",
    "vpk-news.ru",
    "shambalacasino.ru",
    "aeducar.es",
    "webticari.net",
    "amengees.org",
    "antiperekup.com",
    "filmsdream.com",
    "koalia-stories.com",
    "prosperonline.com",
    "regenmesserapp.de",
    "captainrider.fr",
    "menutaiwan.com",
    "textileinfomedia.com",
    "aviewfrommyseat.com",
    "pcmonitors.info",
    "topdesignfirms.com",
    "smartsoftware.com.bd",
    "dziennik.pl",
    "grall.io",
    "transit.511.org",
    "fsc.go.kr",
    "pepsico.co.uk",
    "dusal.blogmn.net",
    "smsbulko.com",
    "planetprof.it",
    "kwezal.com",
    "jyojewellery.com",
    "meetmylovelife.com",
    "absolutepeoplesearch.com",
    "minnasundberg.fi",
    "stradivarius.it",
    "markable.ai",
    "venetoinside.com",
    "gossip.it",
    "culturecheesemag.com",
    "kanchanapisek.or.th",
    "advancedairlines.com",
    "anyway.fm",
    "buildolution.com",
    "rondevanvlaanderen.be",
    "omloophetnieuwsblad.be",
    "greekboston.com",
    "homefiresprinkler.org",
    "primariacraiova.ro",
    "chijmes.com.sg",
    "albanianews.it",
    "brainlife.io",
    "wnycatholic.org",
    "prismboutique.com",
    "radioacktiva.com",
    "melonfarmers.co.uk",
    "rmcr.org",
    "yablor.ru",
    "votesaveamerica.com",
    "deformetrica.org",
    "slowfoodfoundation.com",
    "rusarm.ru",
    "ehlisunnetbuyukleri.com",
    "adaway.org",
    "wow.uscgaux.info",
    "milosz.pl",
    "necliberia.org",
    "aussieairliners.org",
    "artmuza.spb.ru",
    "jornadaonline.com",
    "alerti.com",
    "cfids.org",
    "cloudnord.fr",
    "vayacondios.be",
    "getsymphony.com",
    "uyghurdictionary.org",
    "stgeorge.org.mt",
    "reseaucerta.org",
    "canadanewsmedia.ca",
    "greekstatemuseum.com",
    "sumoforum.net",
    "member.fsf.org",
    "ely.anglican.org",
    "iautmu.ac.ir",
    "bridgeguys.com",
    "hacklido.com",
    "nws.cgaux.org",
    "supremelaw.org",
    "perunamaa.net",
    "mitrails.org",
    "ilquotidianoitaliano.com",
    "kb.corel.com",
    "electronics-tutorials.com",
    "davies.pl",
    "benweyts.be",
    "hammersound.net",
    "minutemirror.com.pk",
    "deltakappagamma.org",
    "helsingintuomiokirkko.fi",
    "jsont.run",
    "taylor.town",
    "geometros.com",
    "jurgenallewijn.nl",
    "pcmag.co.uk",
    "fortancient.org",
    "live.cgaux.org",
    "wiki.geeklog.net",
    "millenniumcohort.org",
    "icdept.cgaux.org",
    "podium.ac.uk",
    "gaepd.org",
    "paulscode.com",
    "sztucznainteligencja.org.pl",
    "netmag.pk",
    "sage-exchange.co.uk",
    "zinkov.com",
    "survol.me",
    "popledge.co.uk",
    "hdept.cgaux.org",
    "mumps-solver.org",
    "margie.la",
    "flipon.net",
    "auxten.com",
    "chaosfurs.social",
    "sporks.gg",
    "botnix.org",
    "sxrekord.com",
    "fkanavati.com",
    "gauthier-thomas.dev",
    "eurthisnthat.com",
    "pianino.es",
    "ieqt.org",
    "meteorites.tv",
    "rocknytt.net",
    "ap-arts.be",
    "arasbaran.org",
    "everythingsondheim.org",
    "integrateplus.org",
    "ningaloowhalesharks.com",
    "pcdvd.com.tw",
    "ppgroup.uscgaux.info",
    "tdept.cgaux.org",
    "indiavisiontv.com",
    "aerotropolisbusinessconcepts.aero",
    "a082.uscgaux.info",
    "stephenfincher.org",
    "gazetaph.ro",
    "gospelnewsnetwork.org",
    "caliburn.nl",
    "wickwerks.com",
    "pdept.cgaux.org",
    "stevedow.com.au",
    "blog-logiciel-btp.com",
    "thetalentedindian.com",
    "dirim.com",
    "exultet-solutions.com",
    "pluezek-esperanto.net",
    "schittkowski.de",
    "stqw.org",
    "therion011.com",
    "netsamurai.de",
    "gaziantepagzi.com",
    "museumplanes.com",
    "lightknights.com",
    "chicanol.com",
    "leandrovieira.com",
    "easypay.co.ug",
    "storeinterfacer.com",
    "dasauge.de",
    "ilmegliodiinternet.it",
    "anadarservices.com",
    "radioradio.it",
    "tropisme.coop",
    "direitodoestado.com.br",
    "chateau-logic.com",
    "iikv.org",
    "vixenvapors.com",
    "unil-opal.com",
    "maths-fi.com",
    "cyberuskey.com",
    "ethnews.com",
    "ardeya.ru",
    "shophandmade.com",
    "communityhomestay.com",
    "brickmarketing.com",
    "ruralgest.net",
    "op-rolletjes-producties.nl",
    "quake.com.my",
    "sakharovcenter-vdu.eu",
    "netvision-digital.com",
    "mintbuilder.com",
    "clubcomex.com",
    "virtualfitnesstrainer.com",
    "tierraenlasmanos.com",
    "posbpassionrunforkids.com",
    "droledexpe.fr",
    "bonprixelectromenagers.com",
    "mathsfi.com",
    "vftnobsfitness.virtualfitnesstrainer.com",
    "darkpistols.com",
    "pukuni.fi",
    "writerstudio.com.sg",
    "drthamer.com",
    "mediamorphosis.ro",
    "sueschlabach.com",
    "madebypaletta.com",
    "robertsonoptical.com",
    "blackhawkvisions.com",
    "sansarpetsupply.com",
    "ateliers-autonomes.com",
    "shirinliving.com",
    "tmailor.com",
    "geekculture.com",
    "webwedmobile.com",
    "thedccenter.org",
    "dia.org.au",
    "twostepsbeyond.com",
    "theoryforce.com",
    "cryptonews.com.au",
    "collegehunkshaulingjunk.com",
    "fasak.com",
    "mediarama.io",
    "kayroslink.com.br",
    "stimart.com",
    "peruschool.com.pe",
    "cuidodevc.com.br",
    "developer.invotra.com",
    "onsexprime.fr",
    "tomatina.es",
    "problemattic.app",
    "faroesoccer.com",
    "biggestloser.com",
    "pagsmile.com",
    "startrankingnow.com",
    "americanhearth.com",
    "rollandplaypress.com",
    "normandiecourseapied.com",
    "ysarc.net",
    "slip32.com",
    "crsa.fr",
    "salz.ch",
    "websiteseochecker.com",
    "garazibaigorri.com",
    "ville-sermaize-les-bains.fr",
    "play.fm",
    "latrucada.cat",
    "staatsbad-salzuflen.de",
    "boxingforum24.com",
    "simplyscripts.com",
    "palabrasdelcandil.com",
    "innovationwomen.com",
    "roleplayingtips.com",
    "briandixon.com",
    "ubuy.ae",
    "fangirlsgoingrogue.com",
    "vigilare.info",
    "souq-design.com",
    "cryptocloud9.io",
    "fnkc.online",
    "blue-iptv.com",
    "rodiongaming.com",
    "netzfrauen.org",
    "lisbonweekendguild.com",
    "lucd.info",
    "blogohblog.com",
    "laguepie.fr",
    "globalrightsindex.org",
    "inkblot.art",
    "giroll.org",
    "liw.fi",
    "klintmarketing.com",
    "kentuckyhealthjusticenetwork.org",
    "losereno.com",
    "janjambon.be",
    "stemitupsports.com",
    "drystonegarden.com",
    "fakefoodjapan.com",
    "sundowners.org.uk",
    "returndates.com",
    "xenomorph.net",
    "block.fm",
    "rostfrei-stahl.com",
    "remeroninfo.com",
    "protonixinfo.com",
    "cdp.solutions",
    "psnews.ro",
    "espcr.org",
    "jessehouwing.net",
    "sneakerbaron.nl",
    "wodka-gorbatschow.de",
    "thaqfny.com",
    "zoo-ag.de",
    "bhcpress.com",
    "aop.plus",
    "strgzh.ch",
    "balser.info",
    "bezahlbarer-wohnraum-osnabrueck.de",
    "dehoogevener.nl",
    "thomastrenkler.at",
    "spreitgraben.ch",
    "conservation-nature.fr",
    "pasionaria.it",
    "boldist.co",
    "retirementjobs.com",
    "wiresoft.ch",
    "isis.org",
    "enterpriserentacar.ca",
    "debrabantsepijl.be",
    "aphekom.org",
    "newpathweb.com.au",
    "chl.kiev.ua",
    "chez-mon-libraire.fr",
    "tempofradi.hu",
    "thecollectin.com",
    "pagerank.net",
    "chinaworker.info",
    "lojaorganiconatural.com.br",
    "informadrid.com",
    "ukropshomestylefoods.com",
    "hostman.com",
    "kumikomi.net",
    "emilyandthesimons.com",
    "asoloartfilmfestival.com",
    "angelagudo.es",
    "geopalz.com",
    "lecourrierdelamayenne.fr",
    "heikniemi.net",
    "mmr.ua",
    "enterprise.ca",
    "emuvr.net",
    "sziklakorhaz.eu",
    "fondazionebasso.it",
    "crescent.cloud",
    "1031.org",
    "jourssa.ru",
    "biosolids.com.au",
    "aldia.com.ec",
    "phonorama.fr",
    "servant-tourisme.com",
    "igarkacity.info",
    "ifthenisnow.nl",
    "orchestramozart.com",
    "sketchub.in",
    "openhousebsas.org",
    "motusmotus.com",
    "restaurant-lapaika.com",
    "info-depression.fr",
    "puravitalosangeles.com",
    "d-central.tech",
    "webdiplomacy.net",
    "heavensentgaming.com",
    "webgraffiti.it",
    "glassbrasserie.com.au",
    "revistagesec.org.br",
    "campsas.fr",
    "30dh.shop",
    "applicature.com",
    "floatplancentral.cgaux.org",
    "pixa.fr",
    "jakpiekniebyckobieta.pl",
    "modvilla.com",
    "cleaningwomen.com",
    "museecapdagde.com",
    "tdmsresearch.com",
    "villes-sanctuaires.com",
    "blackandgold.com",
    "ville-golfech.fr",
    "fullcirclefund.org",
    "uploadboy.com",
    "itrinnovation.com",
    "adfc-mv.de",
    "henriot-quimper.com",
    "comby.org",
    "luttepauvrete.be",
    "durfort-lacapelette.fr",
    "villebrumier.fr",
    "bio-met.net",
    "ville-saint-mathieu-de-treviers.fr",
    "commune-montgon08.com",
    "sol-monnaies-locales.org",
    "centrolulu.com.br",
    "vinilrecords.com.br",
    "medicinescience.org",
    "thewellnesscommunity.org",
    "sentiersderando.fr",
    "real-vin.com",
    "dreampairshoes.com",
    "snd.ps",
    "diceofdoom.com",
    "facts.ch",
    "redpixie.com",
    "organicnz.org.nz",
    "betopick.com",
    "office360.co.in",
    "cjcpga.org",
    "shawnxli.com",
    "ytjobs.co",
    "ltcovid.com",
    "ursa-tm.ru",
    "uunoklami.fi",
    "mairie-pouxeux.com",
    "pays-george-sand.fr",
    "realist.co.th",
    "surewest.com",
    "bidexpress.com",
    "names4ever.nl",
    "acesportsbook.com",
    "dishonline.com",
    "chateaudemontvillargenne.com",
    "crash-aerien.aero",
    "minterapp.com",
    "ura.dn.ua",
    "merles.fr",
    "managementparadise.com",
    "liefdevoorlekkers.nl",
    "stephenramsay.us",
    "performline.com",
    "explorekohchang.com",
    "eyedoctorophthalmologistnyc.com",
    "grupgerminal.org",
    "faudoas.com",
    "fcdawkins.com",
    "c3bs.com",
    "bloghotel.org",
    "portailpalliatif.ca",
    "pearlwestgroup.com",
    "charlijames.com",
    "jeuxvideomagazine.com",
    "whitneystrong.org",
    "femmes-solidaires.org",
    "soundtrackworld.com",
    "treasurefi.com",
    "tac-art.com",
    "compareboilercover.co.uk",
    "1980editions.com",
    "oniblogrank.com",
    "readconmigo.org",
    "impulse-hokkaido.com",
    "anikobranding.com",
    "filieresport.com",
    "camillejullian.com",
    "dekastvanmormon.info",
    "forum-zones-humides.org",
    "kalevala-welt.ru",
    "computertalkradio.com",
    "alcoolinfoservice.fr",
    "ijcs.ro",
    "galeriegng.com",
    "nextincareer.com",
    "artistsupplysource.com",
    "inea.gob.ve",
    "grandmiramor.com.tr",
    "teamheal.org",
    "cg21.fr",
    "ahf-filosofia.es",
    "ednp.ch",
    "rsscalendar.com",
    "3ptechies.com",
    "fishipedia.es",
    "winterkongress.ch",
    "redkit.org",
    "blog-perfumes.pt",
    "buscroatia.com",
    "wildbit-soft.fi",
    "peacemakers.sg",
    "fazzle.com",
    "diyarbakirsoz.com",
    "saintcricqchalosse.fr",
    "lizac.fr",
    "igcseprep.com",
    "daytonconventioncenter.com",
    "pglingua.org",
    "creatif.com",
    "inverses.fr",
    "radicalnetworks.org",
    "ttis.ru",
    "sternclient.biz",
    "thevintageportsite.com",
    "fishing.ne.jp",
    "nato-leipzig.de",
    "kazzuazzee.com.br",
    "fotostate.ru",
    "muletowndigital.com",
    "cheapigfollowers.com",
    "discoverynetworks.nl",
    "adarit.com",
    "coursdeau.be",
    "lc-maillard.org",
    "prathaprachan-mag.com",
    "hoboscafe.net",
    "tadawulfx.com",
    "robertbue.no",
    "nantes-developpement.com",
    "louvino.com",
    "digitalthoughts.science",
    "newenglandwatercolorsociety.org",
    "diariofolk.com",
    "t-shirthumor.com",
    "ilpescatoreonline.it",
    "sandyaveledo.net",
    "khnu.km.ua",
    "finasucre.com",
    "caminobarrancodemasca.com",
    "manilashaker.com",
    "milestonebased.com",
    "congresotipografia.com",
    "supportivy.com",
    "ormuco.com",
    "eitictlabs.eu",
    "wegolo.com",
    "eleykishimoto.com",
    "ashanti.co.za",
    "fmdva.org",
    "unitomo.ac.id",
    "culture-13.fr"
]

def load_lines(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def send_email(args, recipient, from_name, from_email, subject):
    try:
        msg = MIMEMultipart()
        msg['From'] = f"{from_name} <{from_email}>"
        msg['To'] = recipient
        msg['Subject'] = subject
        
        with open(args.html, 'r') as f:
            html_body = f.read()
        
        msg.attach(MIMEText(html_body, 'html'))
        
        with smtplib.SMTP(args.smtp_server, 25) as server:
            server.starttls()
            server.send_message(msg)
        
        print(f"✅ Sent to {recipient}")
        return True
    except smtplib.SMTPResponseException as e:
        if 450 <= e.smtp_code <= 499:
            print(f"🔄 Temporary error for {recipient}: {e.smtp_code}")
            return False
        else:
            print(f"✉️ Bounced from {recipient}: {e.smtp_code} {str(e)}")
            return True
    except Exception as e:
        print(f"⚠️ Failed to send to {recipient}: {str(e)}")
        return True

def send_emails_in_parallel(args, email_list):
    failed_emails = []
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = []
        for recipient, from_name, subject in email_list:
            futures.append(executor.submit(
                send_email, 
                args, 
                recipient, 
                from_name, 
                args.from_email, 
                subject
            ))
            time.sleep(0.1)

        for i, future in enumerate(futures):
            success = future.result()
            if not success:
                failed_emails.append(email_list[i])
    return failed_emails

def main():
    parser = argparse.ArgumentParser(description='Send bulk emails with threading')
    parser.add_argument('--recipients', required=True, help='Path to recipients file')
    parser.add_argument('--html', required=True, help='Path to HTML email template')
    parser.add_argument('--froms', required=True, help='Path to from names file')
    parser.add_argument('--subjects', required=True, help='Path to subject lines file')
    parser.add_argument('--smtp-server', required=True, help='SMTP server address')
    parser.add_argument('--threads', type=int, default=100, help='Number of threads to use')
    parser.add_argument('--max-retries', type=int, default=3, help='Maximum number of retry attempts')
    args = parser.parse_args()

    for f in [args.recipients, args.html, args.froms, args.subjects]:
        if not os.path.exists(f):
            print(f"❌ File not found: {f}")
            exit(1)

    recipients = load_lines(args.recipients)
    from_names = load_lines(args.froms)
    subjects = load_lines(args.subjects)
    
    if not recipients or not from_names or not subjects:
        print("❌ One or more input files are empty")
        exit(1)

    # We will assign domains sequentially per recipient (wrap around)
    total_domains = len(list_of_domains)
    email_list = []
    for idx, recipient in enumerate(recipients):
        from_name = random.choice(from_names)
        subject = random.choice(subjects)
        domain = list_of_domains[idx % total_domains]
        random_id = random.randint(1000, 9999)
        from_email = f"rewards-{random_id}@{domain}"
        email_list.append((recipient, from_name, subject, from_email))

    # Note: each email now has its own from_email, so we cannot use a single args.from_email.
    # We'll modify the parallel sending to use per-email from_email.
    # Since send_email expects args.from_email, we'll pass it as an argument.
    # Let's redefine send_emails_in_parallel to accept a list of tuples with (recipient, from_name, subject, from_email)

    def send_email_with_custom_from(args, recipient, from_name, from_email, subject):
        # Same as send_email but uses provided from_email
        try:
            msg = MIMEMultipart()
            msg['From'] = f"{from_name} <{from_email}>"
            msg['To'] = recipient
            msg['Subject'] = subject
            
            with open(args.html, 'r') as f:
                html_body = f.read()
            
            msg.attach(MIMEText(html_body, 'html'))
            
            with smtplib.SMTP(args.smtp_server, 25) as server:
                server.starttls()
                server.send_message(msg)
            
            print(f"✅ Sent to {recipient} from {from_email}")
            return True
        except smtplib.SMTPResponseException as e:
            if 450 <= e.smtp_code <= 499:
                print(f"🔄 Temporary error for {recipient}: {e.smtp_code}")
                return False
            else:
                print(f"✉️ Bounced from {recipient}: {e.smtp_code} {str(e)}")
                return True
        except Exception as e:
            print(f"⚠️ Failed to send to {recipient}: {str(e)}")
            return True

    def send_emails_in_parallel_custom(args, email_list):
        failed_emails = []
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            futures = []
            for recipient, from_name, subject, from_email in email_list:
                futures.append(executor.submit(
                    send_email_with_custom_from,
                    args,
                    recipient,
                    from_name,
                    from_email,
                    subject
                ))
                time.sleep(0.1)
            for i, future in enumerate(futures):
                if not future.result():
                    failed_emails.append(email_list[i])
        return failed_emails

    print(f"📧 Using sequential domains from list of {total_domains}")
    print(f"📝 Subject: random from subjects file")
    print(f"📨 Total recipients: {len(recipients)}")
    print(f"🧵 Using {args.threads} threads")
    print(f"🔄 Max retries: {args.max_retries}")

    # Initial send
    print("\n📤 Starting initial send...")
    failed_emails = send_emails_in_parallel_custom(args, email_list)
    print(f"Initial send completed. {len(failed_emails)} emails need retry.")

    # Retry loop
    for retry_attempt in range(args.max_retries):
        if not failed_emails:
            break
        print(f"\n🔄 Retry attempt {retry_attempt + 1}/{args.max_retries} with {len(failed_emails)} emails")
        failed_emails = send_emails_in_parallel_custom(args, failed_emails)

    if failed_emails:
        print(f"\n❌ {len(failed_emails)} emails failed after all retry attempts")

    print("\n🎉 Email sending completed!")

if __name__ == "__main__":
    main()