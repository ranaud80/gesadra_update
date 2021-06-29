<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format">
	<!-- 
	style-sheet de présentation des messages DM
	-->

  <!-- Subroutine that replaces a leading space or tab -->
  <!-- with a hard (non-breaking) space -->
  <!-- Input: parameter "str", a string -->
  <!-- Returns: value of "str" w/ leading space replaced -->
<xsl:template name="replace-leading-space">
    <xsl:param name="str"/>
    <xsl:variable name="first" select="substring( $str, 1, 1 )"/>
    <xsl:choose>
        <xsl:when test="$first='&#x20;' or $first='&#x09;'">
            <xsl:value-of select="concat('&#160;', substring( $str, 2 ))"/>
        </xsl:when>
        <xsl:otherwise>
            <xsl:value-of select="$str"/>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>
  
<xsl:output method="html" version="1.0" encoding="ISO-8859-1" indent="yes"/>
<xsl:template match="/">

<html>
	<head>
		<style type="text/css">

table.msg { 
	width: 700px; 
    font-family: Arial, Helvetica, sans-serif;
    border-style: solid; 
	border-width: 1px;
}

table.title { 
	width: 100%;
    font-weight: bold;
	text-align: center;
 }

th.title {
    font-size: 1.2em;
    color: blue
}

td.title {
    font-size: 2em;
}

td.mode {
    color: red;
}

table.pgh {
    width: 100%;
    border-width: 0;
}
th.pgh {
    text-align: center;
    background-color: orange;
    color: blue;
}
td.lib {
	width: 25%;
}

        </style>
    </head>
    <body align="center" width="700px">
            <table class="msg">
				<tr>
					<td>
						<table class="title">
                            <tr>
								<th class="title">ASSOCIATION DEPARTEMENTALE DES RADIOAMATEURS</th>
                            </tr>
                            <tr>
                                <th class="title">AU SERVICE DE LA SECURITE CIVILE</th>
                            </tr>
                            <tr>
                                <td>
                                    <hr size="3" color="blue" />
                                    <hr size="3" color="orange" />
                                </td>
                            </tr>
                            <tr>
                                <td class="title">MESSAGE</td>
                            </tr>
                            <tr>
                                <td class="mode">
                                    <xsl:if test="msg/mode = 'Exercice'">- EXERCICE - EXERCICE - EXERCICE -</xsl:if>
								</td>
							</tr>
						</table>
                        <br/>
						<table class="pgh">
							<tr>
                                <th class="pgh" colspan="2">Informations transmission</th>
                            </tr>    
                            <tr>
								<td class="lib">Groupe Date/Heure</td>
								<td><xsl:value-of select="msg/trans/gdh"/>&#160;</td>
                            </tr>
                            <tr>
								<td class="lib">Emis par</td>
								<td><xsl:value-of select="msg/trans/emis"/>&#160;</td>
                            </tr>
                            <tr>
								<td class="lib">Reçu par</td>
								<td><xsl:value-of select="msg/trans/recu"/>&#160;</td>
							</tr>
                            <tr>
								<td>Instructions particulières</td>
								<td><xsl:value-of select="msg/trans/instr"/>&#160;</td>
							</tr>
                        </table>
                        <br/>
                        <table class="pgh">
                            <tr>
                                <th class="pgh" colspan="2">Message BT</th>
                            </tr>    
							<tr>
								<td class="lib">Origine</td>
								<td><xsl:value-of select="msg/top/from"/>&#160;</td>
                            </tr>    
							<tr>
								<td class="lib">Dest. Action</td>
								<td><xsl:value-of select="msg/top/to"/>&#160;</td>
                            </tr>    
							<tr>
								<td class="lib">Dest. Info</td>
								<td><xsl:value-of select="msg/top/info"/>&#160;</td>
                            </tr>    
							<tr>
								<td class="lib">Urgence</td>
								<td><xsl:value-of select="msg/top/urg"/>&#160;</td>
							</tr>    
                            <tr>
                                <td colspan = "3">
                                    <hr size="3" color="orange" />
                                </td>
                            </tr>
                        </table>
                        <table class="pgh">
                            <tr>
								<td class="lib">Objet</td>
								<td><xsl:value-of select="msg/corps/obj"/>&#160;</td>
							</tr>
                            <tr>
                                <td class="lib">Dépt. alerté et touché</td>
                                <td><xsl:value-of select="msg/corps/dptaet"/>&#160;</td>
                            </tr>							
                            <tr>
                                <td class="lib">Dépt. touché non alerté</td>
                                <td><xsl:value-of select="msg/corps/dpttna"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Dépt. alerté non touché</td>
                                <td><xsl:value-of select="msg/corps/dptant"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Plan ORSEC</td>
                                <td><xsl:value-of select="msg/corps/orsec"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Portée ORSEC</td>
                                <td><xsl:value-of select="msg/corps/portee"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Cellule de crise activée</td>
                                <td><xsl:value-of select="msg/corps/crise"/>&#160;</td>
                            </tr>
                        </table>
                        <br/>
						<table class="pgh">
							<tr>
                                <th colspan="2">Bilan</th>
                            </tr>    
                            <tr>
                                <td class="lib">Nb de décédés</td>
                                <td><xsl:value-of select="msg/corps/ong1/dcd"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Nb de blessés</td>
                                <td><xsl:value-of select="msg/corps/ong1/blesse"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Nb de déplacés/relogés</td>
                                <td><xsl:value-of select="msg/corps/ong1/deplace"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Nb d'interventions</td>
                                <td><xsl:value-of select="msg/corps/ong1/interv"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Hélitreuillés</td>
                                <td><xsl:value-of select="msg/corps/ong1/heli"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Axes coupés</td>
                                <td><xsl:value-of select="msg/corps/ong1/axe"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Foyers privés d'eau</td>
                                <td><xsl:value-of select="msg/corps/ong1/sanseau"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Foyers privés d'électricité</td>
                                <td><xsl:value-of select="msg/corps/ong1/sanselec"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Foyers privés de téléphone</td>
                                <td><xsl:value-of select="msg/corps/ong1/sanstel"/>&#160;</td>
                            </tr>
                        </table>
						<table class="pgh">
							<tr>
                                <th colspan="2">Effectifs</th>
                            </tr> 
							<tr>
								<td class="lib">SP locaux</td>
								<td><xsl:value-of select="msg/corps/ong2/sploc"/>&#160;</td>
							</tr>
							<tr>
								<td class="lib">SP Extra zonaux</td>
								<td><xsl:value-of select="msg/corps/ong2/spext"/>&#160;</td>
							</tr>
							<tr>
								<td class="lib">Militaires Sécurité Civile</td>
								<td><xsl:value-of select="msg/corps/ong2/milsc"/>&#160;</td>
							</tr>
							<tr>
								<td class="lib">Police/Gendarmerie</td>
								<td><xsl:value-of select="msg/corps/ong2/police"/>&#160;</td>
							</tr>
							<tr>
								<td class="lib">Militaires</td>
								<td><xsl:value-of select="msg/corps/ong2/armee"/>&#160;</td>
							</tr>
							<tr>
								<td class="lib">Asso. de Sécurité Civile</td>
								<td><xsl:value-of select="msg/corps/ong2/assosc"/>&#160;</td>
							</tr>
							<tr>
								<td class="lib">EDF/GDF</td>
								<td><xsl:value-of select="msg/corps/ong2/elec"/>&#160;</td>
							</tr>
							<tr>
								<td class="lib">France Télécom</td>
								<td><xsl:value-of select="msg/corps/ong2/telecom"/>&#160;</td>
							</tr>
							<tr>
								<td class="lib">DDE/DIR/CG</td>
								<td><xsl:value-of select="msg/corps/ong2/equip"/>&#160;</td>
							</tr>
                        </table>
						<table class="pgh">
							<tr>
                                <th colspan="2">Moyens</th>
                            </tr>
							<tr>
								<td class="lib">Hélico. Sécurité Civile</td>
								<td><xsl:value-of select="msg/corps/ong3/helisc"/>&#160;</td>
							</tr>
							<tr>
								<td class="lib">Hélico. Militaires</td>
								<td><xsl:value-of select="msg/corps/ong3/helimil"/>&#160;</td>
							</tr>
							<tr>
								<td class="lib">Groupes Electrogènes</td>
								<td><xsl:value-of select="msg/corps/ong3/grpelec"/>&#160;</td>
							</tr>
							<tr>
								<td class="lib">Autres</td>
								<td><xsl:value-of select="msg/corps/ong3/autre"/>&#160;</td>
							</tr>
						</table>
						<table class="pgh">
                            <tr>
                                <th class="pgh" colspan="2">Fin message</th>
                            </tr>    
							<tr>
								<td class="lib">GDH Dépôt</td>
								<td><xsl:value-of select="msg/bot/gdh"/>&#160;</td>
							</tr>
							<tr>
								<td class="lib">Demande A.R.</td>
								<td><xsl:value-of select="msg/bot/ack"/>&#160;</td>
							</tr>
						</table>
                        <br/>
						<table class="title">
                            <tr>
                                <td class="mode">
									<xsl:if test="msg/mode = 'Exercice'">- EXERCICE - EXERCICE - EXERCICE -</xsl:if>
                                </td>
                            </tr>
                            <tr>
                                <td align="right">
                                    <font size="1.5px">
                                        Message BT
                                        <br/>
                                        <xsl:value-of select="msg/soft"/>&#160;<xsl:value-of select="msg/vers"/>
                                    </font>
                                </td>
							</tr>
						</table>
					</td>
				</tr>
			</table>
	</body>
</html>

</xsl:template>
</xsl:stylesheet>
