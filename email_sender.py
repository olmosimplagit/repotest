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
"v53.uk",
"everybodywinsatlanta.org",
"expansionynegocios.com",
"basil.com",
"lavit-de-lomagne.fr",
"bankexam.fr",
"norafrik.com",
"monclar-de-quercy.fr",
"gumrukdeposu.net",
"squidsolutions.com",
"alabs.org",
"vsxu.com",
"mas-grenier.fr",
"barrydislemade.fr",
"monbequi.fr",
"urbian.co.za",
"ekipafanihy.org",
"lethiron.com",
"brandfeatured.com",
"bardigues.fr",
"laurentperezdelmar.com",
"joannlai.com",
"danfa.net",
"floridsdorf.net",
"deepchild.com",
"flirtblog.ch",
"davesieg.com",
"seaviewaquariums.com",
"tohumagazine.com",
"maisondelacravate.fr",
"setupsigning.nl",
"steroidscanada.ca",
"mysecretpantry.com",
"comune.campodipietra.cb.it",
"commune-montcet.fr",
"piraattilahti.fi",
"enterprise.es",
"leatherschool.biz",
"roseboxnyc.com",
"militarytechnics.com",
"yandy-ager.com",
"ontuscia.it",
"godmodehq.com",
"paundurlic.com",
"photoscape.ru",
"fundacionindex.com",
"eduxpert.in",
"hobbiton.org",
"comune.polinago.mo.it",
"matthewwoodard.com",
"mujeresenelsectorpublico.com",
"panperduto.it",
"keebs.com",
"latzinator.com",
"donnerenligne.fr",
"macquarieim.com",
"rainfiremedia.com",
"bestfortmyersrealestate.com",
"gotujzcukiereczkiem.pl",
"dahlemcenter.org",
"kampinkappeli.fi",
"leechermods.com",
"worldwidegreeks.com",
"cyberknights.com.au",
"akteon.fr",
"treouergat.bzh",
"canadiangamingbusiness.com",
"trec.org.tw",
"lifesurferissue.com",
"symmetryptmiami.com",
"skyball.am",
"auty.fr",
"pommevic.fr",
"escazeaux.fr",
"brentter.com",
"frens-haring.nl",
"exbaba.com",
"galerie-pluskwa.com",
"saint-nazaire-de-valentane.fr",
"integralwebsolutions.co.za",
"villemade.fr",
"aps-hl.at",
"freeglisse.com",
"lautremedia.com",
"ultrafun.fr",
"rapidfire.com",
"automania.by",
"poppylist.com",
"nottinghamshire.pcc.police.uk",
"scorchfelix.com",
"jamielesouef.com",
"channelexpo.co.uk",
"afric.info",
"faeca.es",
"mymarchy.com",
"rescoopvpp.eu",
"okfn.se",
"hitachi-displays.com",
"sbcimpact.net",
"carlssonbokforlag.se",
"liesbethhomans.be",
"gothicgame.ru",
"rm-rf.es",
"cenobyte.ca",
"comacina.it",
"helmetstohardhats.com",
"dufferincounty.on.ca",
"ledoutfitters.com",
"somostodosum.com.br",
"epmlive.com",
"sportmagazine.it",
"jividenlaw.com",
"musee-baronmartin.fr",
"africa-news.net",
"turismo.al",
"nanthalaw.com",
"vezelaytourisme.com",
"taistelijantalo.fi",
"bison-transport.eu",
"mecadata.com",
"pixelcoblog.com",
"storiedirally.it",
"foxriverassociates.com",
"partyshop.nl",
"tea-for-two.com",
"webhirad.com",
"e-minbar.com",
"split.it",
"isigny-grandcamp-intercom.fr",
"venetocultura.org",
"tanja24.com",
"pedrolegerpereira.pt",
"pivioworks.com",
"iodocs.com",
"alsurvacaciones.com",
"pinkpigeon.co.uk",
"szczecinlab.pl",
"cheu.fr",
"closertovaneyck.be",
"sportoriginal.by",
"dodochain.com",
"truehealingconference.com",
"hhshootingsports.com",
"sportifun.net",
"saint-emilion-jazz-festival.com",
"canonshoes.com",
"smerep.fr",
"adoteumgatinho.com.br",
"realestateallturkey.com",
"taxi-bateau.com",
"healthvalleyevent.com",
"castlewelt.com",
"litinerant.fr",
"capemploi.info",
"laroussille.com",
"bambini-restaurant.com",
"centreequestreagon.com",
"coca-cola.ba",
"smantics.com",
"jeugdfilmfestival.be",
"turndisposable.store",
"teaonic.com",
"enterpriserentacar.pl",
"serv-u-pharmacy.com",
"royaums.com",
"dreampairs.com",
"thelabellady.shop",
"france-news.net",
"mairie-la-pesse.com",
"qp.com.tr",
"live-radio.ru",
"apilco.com",
"igeek.eu",
"woopit.fr",
"computer-acquisti.com",
"berdskadm.ru",
"onlineg3.com",
"nadp.org.uk",
"les-parfums-de-rosine.com",
"nicolasmanservigi.com.ar",
"gankrin.org",
"sales-pop.carecart.io",
"volzpiano.com",
"slaine.org",
"pimpmynews.com",
"theoutdoorwear.com",
"dansultan.com",
"allgobus.nl",
"comberouger.fr",
"websurveyor.com",
"linekudari.com",
"jonnalee.com",
"coleandkiera.com",
"superpl.us",
"amurbvu.ru",
"whitetail.com",
"monceaux-en-bessin.fr",
"scanimate.net",
"beats-by-dre.co.uk",
"attraction-lemanga.fr",
"moulins-bourgeois.com",
"winterlight.co",
"castelsagrat.fr",
"prednisoneforsale.store",
"etbm.ro",
"star-ice.spb.ru",
"kutaisi.com.ge",
"mainesaves.org",
"professionaladviser.co.uk",
"actualites-electroniques.com",
"koreaopentennis.com",
"biodiversitesousnospieds.fr",
"stables52.com",
"cci-news.com",
"jiz-muenchen.de",
"runforplanet.fr",
"vanlocker.co.uk",
"jeffestival.be",
"iancarterdesigns.com",
"theuy.nl",
"aquiladigital.us",
"barcelonadronecenter.com",
"haulmont.ru",
"nashvillesportsleagues.com",
"technobrains.in",
"museeagathois.fr",
"enterprise.ie",
"devcustom.net",
"info-meningocoque.fr",
"icoi.net",
"associationaudrey.fr",
"dandelion.org",
"my-brussels.com",
"reflymusic.com",
"hobbyscoop.nl",
"estiri.ro",
"letspartysalinas.com",
"vondels.com",
"gweeds.net",
"littletrousers.com",
"shopandbox.com",
"valdealgorfa.com",
"a09116.uscgaux.info",
"naramore.net",
"kenja-succession.com",
"genertec.com.cn",
"chatbot4u.com",
"festivalcasteldeimondi.it",
"vidinst.nl",
"rzekazdrowia.pl",
"hexelon.com",
"mathilderoussel.com",
"theraces.com.au",
"saint-vincent-lespinasse.fr",
"ourworkshop-shop.co.uk",
"ftcbk.eu",
"elfstedentocht.frl",
"forthecloset.co.uk",
"saint-paul-despis.fr",
"photomuseum.lviv.ua",
"tnsny.org",
"pointburst.com",
"palaparing.id",
"baobabexpress.org",
"terre-asile-tunisie.org",
"macquarieresearch.com",
"olcso.hu",
"mscrossroads.org",
"mairie-chalamont.org",
"labastide-du-temple.fr",
"voicesofnote.org",
"savenes.fr",
"beachlifefitnessboutique.com",
"hostelhelsinki.fi",
"dhantuchova.com",
"bootyreader.com",
"tekmarcontrols.com",
"cyme.cloud",
"yun-berlin.com",
"xharbour.com",
"parallax.fr",
"sonsonero.com",
"kreisverein-gp.de",
"lucasgreen.ca",
"network23.com",
"liberdademg.com.br",
"datbooster.com",
"eeko-factory.fr",
"lafitte82.fr",
"twi.org.pl",
"22bit.tv",
"pzsw.waw.pl",
"adaptic.cz",
"ntl.nectec.or.th",
"comune.rionerosannitico.is.it",
"openbouquet.io",
"bittwiddlegames.com",
"afravih2018.org",
"dalsantv.net",
"bonro.de",
"puylaroque.com",
"aucamville.fr",
"happyfitdog.com",
"zuhaldemir.be",
"jrp-next.com",
"lumieres-studio.com",
"haiguinet.com",
"murphysoldtimersmuseum.com",
"doxycyclineonline.store",
"eskaapi.com",
"stampay.com",
"swiftassess.com",
"valbonne.fr",
"vetbionet.eu",
"ropeway.kinu1.com",
"astromedia.com.my",
"vallee-de-la-sarthe.com",
"ces-shop.eu",
"madmaxadventures.com",
"pedacosdavida.com",
"apuestaslegales.co",
"rockthenight.eu",
"miantro.com",
"youngmusicmakers.co.uk",
"solarassetmanagement.us",
"champstudy.com",
"docsvalencia.com",
"saisdfoundation.com",
"jje.go.kr",
"bookishclub.com",
"gheme.com",
"livewithinfo.com",
"luckycatrescue.com",
"akinator.mobi",
"sinaisdostempos.org",
"savethemarriage.com",
"fluttercoin.us",
"childf.com",
"jmais.com.br",
"manjaro-linux.com.br",
"mindthetrip.it",
"solcanafitness.com",
"sakaetp.ne.jp",
"compostelle2000.org",
"rc-plus.net",
"chessinschools.us",
"pamug.org",
"cleanenergyworks.us",
"les-rigolettes-nantaises.com",
"tecidoskite.com.br",
"wilkintie.com",
"shalommemorial.org",
"lefugeret.com",
"netleaseworld.com",
"cap-neree.fr",
"compar.info",
"jeepeg.com",
"gcamenagement.com",
"culturerapide.com",
"olivier-roellinger.com",
"pablocots.net",
"dolls2u.com",
"safagridees.com",
"artisansrose.com",
"georgiaepd.org",
"paisea.com",
"fundacionicbc.com.ar",
"iowadefensecounsel.org",
"data-trading.com",
"netcodepool.org",
"whitelist.tv",
"samuizoom.com",
"contadoresdehistorias.com.br",
"mairie-carency.fr",
"cimalp.es",
"shahsavanseir.com",
"insurance90.com",
"parish.academy",
"artuniverse.eu",
"vazerac.fr",
"boosterdureemploi.immo",
"caue54.fr",
"heartbandits.com",
"rcep7.org",
"laundeabbey.org.uk",
"fullcracksetup.com",
"yummies.com",
"pastishenribardouin.com",
"racowireless.com",
"thebrandguide.com",
"gordianknotbook.com",
"pgdesign.us",
"nortiv8shoes.com",
"mustila.com",
"kibu.ac.ke",
"digital-aarena.com",
"parcs-france.com",
"cleancompany.com",
"shop.fratello.com",
"jurnalulph.ro",
"montefowler.com",
"foresight.fi",
"galileowebcast.hu",
"getyoursockout.co.uk",
"autismhopealliance.org",
"lavaurette.fr",
"lighttherapyhome.com",
"salle-location-avallrich.com",
"dramitabhasaha.com",
"qahc.org.au",
"jfk-stemwede.de",
"keolis-paysduforez.com",
"theartshopltd.com",
"milk-store.com",
"f135.com",
"giftvoucherkiosk.com",
"lthe.fr",
"leviatanscans.com",
"atelierdufuturpapa.com",
"botrail.org",
"walkmanproject.com",
"wiserweb.co.uk",
"belotecardgame.com",
"superstickers.com",
"benscarts.com",
"cerberus-testing.org",
"ablancourt.fr",
"ritadeaninabbeymuseum.org",
"diatribe.us",
"bim.org.bd",
"cefa-rennes.fr",
"crs.org.pl",
"debbiefrank.com",
"theofrancken.be",
"bredevoort-boekenstad.nl",
"femeninafm.cl",
"enterprise.fr",
"harborofgracerecovery.com",
"mykidslink.com",
"elfuturosolar.com",
"emailbean.com",
"rsvm.de",
"viata.es",
"bawkbox.com",
"garfieldhousing.org",
"traffictutors.com",
"centredessinpresse-stjust.com",
"originesbyceline.be",
"teamcast.com",
"collectpure.com",
"goodassur.com",
"legacy.closertovaneyck.be",
"whatsbeef.net",
"kondo.hu",
"tfsfonayliyarismalar.org",
"sslazionuoto.it",
"creationism.org.pl",
"growzer.com",
"hito-oshi.com",
"allcalltechnologies.com",
"decen.com.mx",
"caerfaifarm.co.uk",
"chatspike.net",
"bizmag.co.uk",
"lertthanee.com",
"comicdealer.de",
"theapkwire.com",
"thekingpins.com",
"holapueblo.com",
"w8lrk.org",
"catherinearmstrong.com.au",
"vinobuono.net",
"mylearning.asce.org",
"tmp-mail.pro",
"unium.ru",
"vogania.com",
"estudidentalbarcelona.com",
"fridaysforfuture-saarland.de",
"deaddrunkdublin.com",
"roads-and-rivers.com",
"allnumis.ro",
"jsterlings.com",
"kingandgodfree.com.au",
"triviabot.co.uk",
"enterpriserentacar.it",
"syd24.com",
"wikilovesmuseums.com",
"studentenfondsbertbokxem.nl",
"mapiaule.com",
"plus-forum.com",
"inwebwetrust.org",
"krcmic.cz",
"htlhotels.com",
"christelleperrin.com",
"iniciativaempresarial.es",
"theauthorlife.com",
"baltoscandal.ee",
"carbotti.it",
"guzet.ski",
"climaxthemes.org",
"feaga.org",
"mailboxseattle.com",
"tnpride.com",
"coveyrise.net",
"outranklabs.com",
"pantinclassic.org",
"e-kanu.de",
"b-e-s-team.com",
"tonisoto.com",
"melvados.com",
"mad-cov2.eu",
"masterseo.or.id",
"chrmonshainaut.be",
"zeramusiccompany.com",
"anthem.gr",
"pangaeaproject.org",
"hiza.xyz",
"terijoki.fi",
"apartamentywpolsce.pl",
"gotrackin.com",
"spotonlancashire.co.uk",
"stewardsofchange.com",
"sparte-project.eu",
"lieveblancquaert.be",
"dhormockery.com",
"thechocomonarch.com",
"mechelen.weleer.be",
"sophiedewit.be",
"struikelstenenvalkenburg.nl",
"woneninmortsel.be",
"vincentvandervoort.nl",
"lecardiologue.com",
"lennart-riecken.de",
"namucursos.com.br",
"sunbites.co.uk",
"listyourself.net",
"ferrominera.com",
"zig-star.com",
"regieroutman.com",
"jamiebatchelor.uk.eu.org",
"shop.cardiffstudents.com",
"invitethemedia.com",
"caradriel.com",
"roozmenu.com",
"petlas.com",
"brain-mind.fi",
"successacademy.biz",
"brunomarc.com",
"erenpreiss.com",
"jusdaglobal.com",
"casagoyo.es",
"electroniccigarettesreviews.net",
"atmosfair.fr"
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