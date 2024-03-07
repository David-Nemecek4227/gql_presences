import strawberry as strawberryA

###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################
#
# priklad rozsireni UserGQLModel
#


#     zde je rozsireni o dalsi resolvery¨
#     async def external_ids(self, info: strawberryA.types.Info) -> List['ExternalIdGQLModel']:
#         result = await resolveExternalIds(session,  self.id)
#         return result


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

# 264 - 267
    # volat funkci
    #

    # radnomPresenceData
    # async def ....
    # zavolat funkci
    # předat výstup výsledku dotazu
    # vrátit hlavní datovou strukturu
    # resolvePresenceModelById


###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################
from .Query import Query
from .externals import UserGQLModel
from .externals import EventGQLModel
from .TaskGQLModel import TaskGQLModel
from .Mutation import Mutation

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel, EventGQLModel), mutation=Mutation)
