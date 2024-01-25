import logging
import math
import sys
import time
import requests
from apiai import apiai
from pandas._libs import json
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    Updater,
)
#Permet d'aller chercher le token dans le fichier du même dossiers
token = sys.argv[1]

# PERMET LA CONNEXION
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

STATE_typeSorti, STATE_SortiChoix, STATE_SortiDetails, STATE_RestoChoix, STATE_INFO_RESTO,STATE_RestoDetails,STATE_transport,botai = range(8)

#FONCTION DE LANCEMENT

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""

    #Les choix pour le premiers

    reply_keyboard = [["Sorti", "Restaurant"]]

    #le message de réponse

    await update.message.reply_text(
        "Bonjour ! 👍 Je suis NoctiBot mon but est de t'aider.\n "
        "Envoi /cancel pour ne plus parler avec moi.\n\n"
        "Tu veux aller au resteau ou sortir ?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )
    return STATE_typeSorti


#PERMET DE CHOISIR SI ON SORT DEHORS OU GO RESTO
async def proposer_sorties(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    reply_keyboard = [["Bars", "Musée", "Clubs", "Restaurant"]]

    await update.message.reply_text(
        "Très bien ! Voici les types de sorti qu'on propose ce soir : ",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Bar, Musée ,Club, restaurant"
        ),
    )
    return STATE_SortiChoix


#Permet de choisir sa reco pour sa sortie
async def Sortichoix_Bars(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    reply_keyboard = [["Roller mini Golf bar", "Little Barrel", "L'interdit", "Le brasseur", "Sorti"]]

    await update.message.reply_text(
        "Le brasseur est la brasserie la plus coté à genève elle a une variété de choix imbatable ",
    )
    await update.message.reply_text(
        "l\'interdit est un bar avec une ambiance unique",
        reply_markup=ReplyKeyboardMarkup(
        ),
    )
    await update.message.reply_text(
        "Little barrel est une bar avec des cocktails incroyables",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )
    await update.message.reply_text(
        "Roller mini Golf bar est un endroit unique, vous pouvez profitez avec vos amis tout en jouant au mini golf",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )
    return STATE_SortiDetails
async def Sortichoix_Clubs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    reply_keyboard = [["Usine", "Village du soir", "Le baroque", "Le moulin rouge", "Sorti"]]

    await update.message.reply_text(
        "L'usine est une des plus vieilles boites underground de geneve ",

    )
    await update.message.reply_text(
        "Le village du soir est la plus grande boite de nuit commericial",

    )
    await update.message.reply_text(
        "Le baroque club est une des plus grosse boite coté univers du luxe",

    )
    await update.message.reply_text(
        "le moulin rouge est une des boites les plus populaires auprès des jeunes",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )
    return STATE_SortiDetails
async def Sortichoix_Musee(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    reply_keyboard = [["Musée d'ethnographie de Genève", "Maison tavel", "MAMCO", "Sorti"]]

    await update.message.reply_text(
        "La maison travel est la pour promouvoir l'architecture médival suisse",

    )
    await update.message.reply_text(
        "Le MAMCO est un musée d'art moderne et contemporain",

    )
    await update.message.reply_text(
        "Le musée ethnographie faire des représentation et expostions unique en Suisse Romande ",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
            input_field_placeholder="Musée d'ethnographie de Genève, Maison tavel, MAMCO"
        ),
    )
    return STATE_SortiDetails


#Permet de choisir sa reco de SORTI
async def details_clubs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    reply_keyboard = [["Tout bon", "Restaurant"]]
    await update.message.reply_text(
        "L'usine est une boite de nuit qui est atypique et avec un univers underground",
    )
    await update.message.reply_text(
        "Le village du soir est une des plus grosse boite commercial de genève ",
    )
    await update.message.reply_text(
        "le baroque club est une des boites les plus luxeuxes de Genève",
    )
    await update.message.reply_text(
        "Voulez-vous encore faire une recherche ou s'arreter ici ?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )
    return STATE_INFO_RESTO
async def details_bars(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    reply_keyboard = [["Tout bon", "Restaurant"]]
    await update.message.reply_text(
        "Le brasseur est la brasserie la plus coté à genève elle a une variété de choix imbatable ",
    )
    await update.message.reply_text(
        "l'interdit est un bar avec une ambiance unique ",
    )
    await update.message.reply_text(
        "Little barrel est une bar avec des cocktails incroyables ",
    )
    await update.message.reply_text(
        "Le roller mini gold bar est unique avec son mini golf",
    )

    await update.message.reply_text(
        "Voulez-vous encore faire une recherche ou s'arreter ici ?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )

    return STATE_INFO_RESTO
async def details_musee(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    reply_keyboard = [["Tout bon", "Restaurant"]]
    await update.message.reply_text(
        "Le MAMCO est une musée pour les jeunes par les jeunes ",
    )
    await update.message.reply_text(
        "C'est un musée d'art et d'histoire qui témoigne de l'architecture civil médieval"
    )
    await update.message.reply_text(
        "Le musée unique en suisse démontre les mémoires, l'open data et bien d'autre expositions encore ",
    )

    await update.message.reply_text(
        "Voulez-vous encore faire une recherche ou s'arreter ici ?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )
    return STATE_INFO_RESTO
#Permet de faire son choix de Resto
async def typeSorti_Restaurant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    reply_keyboard = [["italien", "japonais", "français", "americain", "gastronomique"]]

    await update.message.reply_text(
        "Très bien ! Voici les types de restaurant qu'on propose : ",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="italien, japonais, français, anericain, gastronomique"
        ),
    )
    return STATE_RestoChoix


#Permet de choisir sa recomendation de RESTO
async def RestoResultat_italien(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user

    reply_keyboard = [["vino olio caffé", "Spinella", "Marino", "Autre Restaurant"]]
    await update.message.reply_text(
        "marino est une pro de la cusinie bistronomique dit à l'italienne",
    )
    await update.message.reply_text(
        "Spinella est un expert en pizza et est reconnu dans tout Genève",
    )
    await update.message.reply_text(
        "Vino et olio est un spéicaliste de la cusinie tradionelle italienne: ",
        reply_markup=ReplyKeyboardMarkup(
        ),
    )
    return STATE_RestoDetails
async def RestoResultat_japonais(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user

    reply_keyboard = [["Izumi", "Kamome", "Kakinuma", "Autre Restaurant"]]

    await update.message.reply_text(
        "Izumi  Restaurant japonais chic avec sur la ville depuis le toit du Four Seasons Hotel ",

    )
    await update.message.reply_text(
        "Le Kamome, notre restaurant japonais au Mövenpick Hotel Geneva, vous enchantera par la fraicheur et la qualité de ses sushis: ",

    )
    await update.message.reply_text(
        "le Restaurant Kakinuma propose une cuisine et un service traditionnel japonais au plus haut niveau de qualité et d'authenticité ",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Izumi, Kamome, Kakinuma"
        ),
    )
    return STATE_RestoDetails
async def RestoResultat_français(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user

    reply_keyboard = [["L'apparté", "Le Bistroquet", "L'agape", "Autre Restaurant"]]


    await update.message.reply_text(
        "l'apprté est un restaurant étoilé au bord du lac",

    )
    await update.message.reply_text(
        "Bistroquet une cuisine gourmande et authtique digne de la bistronomie française ",

    )
    await update.message.reply_text(
        "agape propose une carte à 2 saisons avec des offrs aussi variées que ses produits",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="L'apparté, Le Bistroquet, L'agape"
        ),
    )
    return STATE_RestoDetails
async def RestoResultat_americain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user

    reply_keyboard = [["Inglewood", "Together", "American Dream Diner", "Autre Restaurant"]]


    await update.message.reply_text(
        "Fast Food Américain d'une chaine de restauration Suisse",

    )
    await update.message.reply_text(
        "American dream diner comme dans son nom est le lieu idéal pour manger comme un américain",

    )
    await update.message.reply_text(
        "together fait des burgers maison, ainsi que du poulet frit",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Inglewood, Together, American Dream Diner"
        ),
    )
    return STATE_RestoDetails
async def RestoResultat_gastronomique(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user

    reply_keyboard = [["The Indus", "Indian Bites", "SUAHOY", "Autre Restaurant"]]

    await update.message.reply_text(
        "Indus près du mont blanc est un restaurant gastronomique à genève dit classique",

    )
    await update.message.reply_text(
        "Si vous devez manger indien, c'est à cette endroit que vous devez venir",

    )
    await update.message.reply_text(
        "Suahoy est un bistrot thai qui offre des recette authentiques et d'auter produits naturelles",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Izumi, Kamome, Kakinuma"
        ),
    )
    return STATE_RestoDetails


#Permet d'avoir les détails du resto
async def details_vino_olio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user

    reply_keyboard = [["Tout bon","Restaurant"]]
    await update.message.reply_text(
        "Un restaurant italien classique offrant une large sélection de vins italiens, des huiles d'olive de qualité et un café authentique. Parfait pour les amateurs de la cuisine traditionnelle italienne",

    )
    await update.message.reply_text(
        "Voulez-vous encore faire une recherche ou s'arreter ici ?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )

    return STATE_INFO_RESTO
async def details_spinella(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user

    reply_keyboard = [["Tout bon","Restaurant"]]
    await update.message.reply_text(
        " Probablement un charmant bistro italien, où vous pourriez déguster de délicieuses pizzas artisanales et des pâtes maison dans une ambiance conviviale",

    )
    await update.message.reply_text(
        "Voulez-vous encore faire une recherche ou s'arreter ici ?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )

    return STATE_INFO_RESTO
async def details_marino(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user

    reply_keyboard = [["Tout bon","Restaurant"]]
    await update.message.reply_text(
        " Un nom qui suggère des spécialités de fruits de mer à l'italienne. Idéal pour ceux qui cherchent à combiner les saveurs de la mer avec la cuisine italienne",

    )
    await update.message.reply_text(
        "Voulez-vous encore faire une recherche ou s'arreter ici ?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )

    return STATE_INFO_RESTO
async def details_izumi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user

    reply_keyboard = [["Tout bon","Restaurant"]]
    await update.message.reply_text(
        "Un restaurant japonais raffiné, probablement spécialisé dans les sushis et sashimis frais, avec une ambiance zen et élégante.",

    )
    await update.message.reply_text(
        "Voulez-vous encore faire une recherche ou s'arreter ici ?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )

    return STATE_INFO_RESTO
async def details_kamome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user

    reply_keyboard = [["Tout bon","Restaurant"]]
    await update.message.reply_text(
        "un restaurant japonais avec une touche contemporaine, offrant une variété de plats japonais modernes et traditionnels.",

    )
    await update.message.reply_text(
        "Voulez-vous encore faire une recherche ou s'arreter ici ?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )

    return STATE_INFO_RESTO
async def details_kakinuma(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user

    reply_keyboard = [["Tout bon","Restaurant"]]
    await update.message.reply_text(
        "un restaurant japonais authentique, peut-être spécialisé dans la cuisine de Kyoto ou dans des plats à base de tempura",

    )
    await update.message.reply_text(
        "Voulez-vous encore faire une recherche ou s'arreter ici ?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )

    return STATE_INFO_RESTO
async def details_apparte(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user

    reply_keyboard = [["Tout bon","Restaurant"]]
    await update.message.reply_text(
        "Un bistro français intime et charmant, parfait pour une soirée romantique avec des plats classiques français.",

    )
    await update.message.reply_text(
        "Voulez-vous encore faire une recherche ou s'arreter ici ?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )

    return STATE_INFO_RESTO
async def details_bistroquet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user

    reply_keyboard = [["Tout bon","Restaurant"]]
    await update.message.reply_text(
        "Un bistro décontracté offrant une cuisine française traditionnelle dans une atmosphère conviviale et accueillante.",

    )
    await update.message.reply_text(
        "Voulez-vous encore faire une recherche ou s'arreter ici ?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )

    return STATE_INFO_RESTO
async def details_inglewood(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user

    reply_keyboard = [["Tout bon","Restaurant"]]
    await update.message.reply_text(
        " Un diner américain avec un accent sur les hamburgers gourmets, les frites maison et les milkshakes classiques.",

    )
    await update.message.reply_text(
        "Voulez-vous encore faire une recherche ou s'arreter ici ?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )

    return STATE_INFO_RESTO
async def details_agarpe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user

    reply_keyboard = [["Tout bon","Restaurant"]]
    await update.message.reply_text(
        "Un restaurant qui promet une expérience gastronomique française, avec des plats raffinés et une excellente sélection de vins.",

    )
    await update.message.reply_text(
        "Voulez-vous encore faire une recherche ou s'arreter ici ?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )

    return STATE_INFO_RESTO
async def details_together(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user

    reply_keyboard = [["Tout bon","Restaurant"]]
    await update.message.reply_text(
        "Un restaurant américain convivial, idéal pour les groupes et les familles, offrant peut-être des plats tex-mex ou des barbecues.",

    )
    await update.message.reply_text(
        "Voulez-vous encore faire une recherche ou s'arreter ici ?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )

    return STATE_INFO_RESTO
async def details_DreamDinner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user

    reply_keyboard = [["Tout bon","Restaurant"]]
    await update.message.reply_text(
        "Un diner rétro américain, parfait pour une expérience nostalgique avec des classiques comme des burgers, des hot-dogs",

    )
    await update.message.reply_text(
        "Voulez-vous encore faire une recherche ou s'arreter ici ?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )

    return STATE_INFO_RESTO
async def details_indus(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user

    reply_keyboard = [["Tout bon","Restaurant"]]
    await update.message.reply_text(
        "Un restaurant indien élégant, spécialisé dans les plats du nord de l'Inde, avec une ambiance chaleureuse et des épices soigneusement sélectionnées.",

    )
    await update.message.reply_text(
        "Voulez-vous encore faire une recherche ou s'arreter ici ?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )

    return STATE_INFO_RESTO
async def details_indian_bite(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user

    reply_keyboard = [["Tout bon","Restaurant"]]
    await update.message.reply_text(
        "Probablement un snack indien rapide et décontracté, parfait pour les déjeuners rapides ou les collations épicées",

    )
    await update.message.reply_text(
        "Voulez-vous encore faire une recherche ou s'arreter ici ?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )

    return STATE_INFO_RESTO
async def details_suahoy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    reply_keyboard = [["Tout bon","Restaurant"]]
    await update.message.reply_text(
        "un restaurant indien moderne, peut-être avec une fusion d'autres cuisines asiatiques",

    )
    await update.message.reply_text(
        "Voulez-vous encore faire une recherche ou s'arreter ici ?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )

    return STATE_INFO_RESTO

#Permet d'annuler l'échange avec le bot
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    await update.message.reply_text(
        "Salut ! J'espère on se reverra.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END
#Permet d'avoir plus d'information
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    await update.message.reply_text(
        "Salut ! Voici les infos supplémentaire qu'on a pour toi :\n\n /transport pour avoir des infos sur les TPG autour de toi ou à un arret précis\n\n  /start pour discuter avec moi et voir ou tu peux aller ce soir !", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

#FONCTION BOT DE TRANSPORT
def appeler_opendata(path):
    url = f"http://transport.opendata.ch/v1{path}"
    reponse = requests.get(url)
    return reponse.json()
def rechercher_arrets(parametres):
    data = appeler_opendata(parametres)
    arrets = data['stations']
    message_texte = "Voici les résultats:\n"

    for arret in arrets:
        if arret['id']:
            message_texte = f'{message_texte}\n /s{arret["id"]}'
            message_texte = f'{message_texte} {arret["name"]}'
            message_texte = f'{message_texte} ({arret["icon"]})'

    return message_texte
def rechercher_prochains_departs(id):

    data = appeler_opendata(f'/stationboard?id={id}')
    stationboard = data['stationboard']

    message_texte = "Voici les prochains départs:\n"
    maintenant = time.time()

    for depart in stationboard:
        message_texte += f"\n\n{depart['number']} → {depart['to']}\n"

        timestamp_depart = depart['stop']['departureTimestamp']
        diff = timestamp_depart - maintenant
        temps_en_minutes = math.floor(diff/60)

        if temps_en_minutes < 0:
            message_texte += ' Déjà parti...'
        elif temps_en_minutes < 2:
            message_texte += ' COURS!'
        else:
            message_texte += f' dans {temps_en_minutes} minutes'

    return message_texte
async def transport(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

    return STATE_transport
async def recherche_texte(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    texte_a_rechercher = update.message.text
    arrets = rechercher_arrets(f'/locations?query={texte_a_rechercher}')
    await update.message.reply_text(arrets)
async def recherche_gps(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_location = update.message.location
    arrets = rechercher_arrets(f'/locations?x={user_location.latitude}&y={user_location.longitude}')
    await update.message.reply_text(arrets)
async def afficher_arret(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    identifiant = update.message.text[2:]
    prochains_departs = rechercher_prochains_departs(identifiant)
    await update.message.reply_text(prochains_departs)

# Processing commands
def startCommand (update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.bot.send_message(chat_id=update.message.chat_id, text='Salut tu veux parler ?')
    return botai
def textMessage (update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = apiai.ApiAI ('clé open ai'). text_request () # Token API to Openai
    request.lang = 'fr' # In which language will the request be sent
    request.session_id = 'asst_Iz8RaoMwUOPRwAlea2ec8sS3'  # ID Sessions
    request.query = Update.message.text # We send a request to the AI with a message from the user
    responseJson = json.loads (request.getresponse (). read (). decode ('utf-8'))
    response = responseJson ['result'] ['fulfillment'] ['speech'] # We parse JSON and pull out the answer
    # If there is an answer from the bot - we send it to the user, if not - the bot did not understand it
    if response:
        context.send_message (chat_id = Update.message.chat_id, text = response)
    else:
        context.send_message (chat_id = Update.message.chat_id, text = 'Je n\'ai pas compris!')



#FONCTION MAIN
def main() -> None:
    """Run the bot."""
    # mon token
    application = Application.builder().token(token).build()

    # Add conversation handler with the state
    conv_handler = ConversationHandler(
        #La commande qui permet de lancer le chat si vous n'avez pas déjà entamer la conversation
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("transport", transport),
            CommandHandler("cancel", cancel),
            CommandHandler("help", help),
            CommandHandler("bot", startCommand)
        ],
        states={
            STATE_typeSorti: [
                MessageHandler(filters.Regex("^(Restaurant)$"), typeSorti_Restaurant),
                MessageHandler(filters.Regex("^(Sorti)$"), proposer_sorties)
            ],
            STATE_SortiChoix: [
                MessageHandler(filters.Regex("^(Restaurant)$"), typeSorti_Restaurant),
                MessageHandler(filters.Regex("^(Bars)$"), Sortichoix_Bars),
                MessageHandler(filters.Regex("^(Musée)$"), Sortichoix_Musee),
                MessageHandler(filters.Regex("^(Clubs)$"), Sortichoix_Clubs)
            ],
            STATE_SortiDetails: [
                MessageHandler(filters.Regex("^(Usine)$"), details_clubs),
                MessageHandler(filters.Regex("^(Village du soir)$"), details_clubs),
                MessageHandler(filters.Regex("^(Le baroque)$"), details_clubs),
                MessageHandler(filters.Regex("^(Le moulin rouge)$"), details_clubs),
                MessageHandler(filters.Regex("^(Little Barrel)$"), details_bars),
                MessageHandler(filters.Regex("^(L'interdit)$"), details_bars),
                MessageHandler(filters.Regex("^(Le brasseur)$"), details_bars),
                MessageHandler(filters.Regex("^(Roller mini golf bar)$"), details_bars),
                MessageHandler(filters.Regex("^(Musée d'ethnographie de Genève)$"), details_musee),
                MessageHandler(filters.Regex("^(Maison tavel)$"), details_musee),
                MessageHandler(filters.Regex("^(MAMCO)$"), details_musee),
                MessageHandler(filters.Regex("^(Sorti)$"), proposer_sorties),
            ],
            STATE_RestoChoix: [
                MessageHandler(filters.Regex("^(italien)$"), RestoResultat_italien),
                MessageHandler(filters.Regex("^(japonais)$"), RestoResultat_japonais),
                MessageHandler(filters.Regex("^(français)$"), RestoResultat_français),
                MessageHandler(filters.Regex("^(americain)$"), RestoResultat_americain),
                MessageHandler(filters.Regex("^(gastronomique)$"), RestoResultat_gastronomique),
                MessageHandler(filters.Regex("^(Autre Restaurant)$"), RestoResultat_gastronomique),
            ],
            STATE_INFO_RESTO: [
                MessageHandler(filters.Regex("^(Restaurant)$"), typeSorti_Restaurant),
                MessageHandler(filters.Regex("^(Tout bon)$"), cancel),
            ],
            STATE_RestoDetails: [
                MessageHandler(filters.Regex("^(Restaurant)$"), typeSorti_Restaurant),
                MessageHandler(filters.Regex("^(Autre Restaurant)$"), typeSorti_Restaurant),
                MessageHandler(filters.Regex("^(vino olio caffé)$"), details_vino_olio),
                MessageHandler(filters.Regex("^(Spinella)$"), details_spinella),
                MessageHandler(filters.Regex("^(Marino)$"), details_marino),
                MessageHandler(filters.Regex("^(Izumi)$"), details_izumi),
                MessageHandler(filters.Regex("^(Kamome)$"), details_kamome),
                MessageHandler(filters.Regex("^(Kakinuma)$"), details_kakinuma),
                MessageHandler(filters.Regex("^(L'apparté)$"), details_apparte),
                MessageHandler(filters.Regex("^(Le Bistroquet)$"), details_bistroquet),
                MessageHandler(filters.Regex("^(L'agape)$"), details_agarpe),
                MessageHandler(filters.Regex("^(Inglewood)$"), details_inglewood),
                MessageHandler(filters.Regex("^(Together)$"), details_together),
                MessageHandler(filters.Regex("^(American Dream Dinner)$"), details_DreamDinner),
                MessageHandler(filters.Regex("^(The Indus)$"), details_indus),
                MessageHandler(filters.Regex("^(Indian Bites)$"), details_indian_bite),
                MessageHandler(filters.Regex("^(SUAHOY)$"), details_suahoy),
            ],
            STATE_transport: [
                MessageHandler(filters.COMMAND, afficher_arret),
                MessageHandler(filters.LOCATION, recherche_gps),
                MessageHandler(filters.TEXT, recherche_texte)
            ],
            botai:[
                # Permet de lancer la conversationa avec l'agent gpt
                CommandHandler('start', startCommand),
                MessageHandler(filters.TEXT, textMessage),
                # Getting Started for Updates
                Updater.start_polling(textMessage),

            ],
        },
        #si dans un des etas d'avant mets cancel pour rappeller la fonction d'avant
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
