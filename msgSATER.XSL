<?xml version="1.0" encoding="UTF-8"?><xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format">
	<!-- 
	style-sheet de présentation des messages BILAN SECOURISTE
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
    font-size: .8em;
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
td.zone {
	width: 28%;
}
td.val {
	width: 8%;
    text-align: center;
}

        </style>
        <script language="Javascript">
            function imp1(){window.print();}
            function imp2(){
                var targetElement;
                targetElement = document.getElementById('1') ;
                targetElement.style.display = "none" ;
                targetElement = document.getElementById('2') ;
                targetElement.style.display = "none" ;
                window.print();
                }
        </script>
    </head>
    <body align="center" width="700px">
            <table class="msg">
				<tr>
					<td>
						<table class="title" id="1">
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
						<table class="pgh">
							<tr>
                                <th class="pgh" colspan="2">Informations transmission</th>
                            </tr>    
                            <tr>
								<td class="lib">Groupe Date/Heure :</td>
								<td><xsl:value-of select="msg/trans/gdh"/>&#160;</td>
                            </tr>
                            <tr>
								<td class="lib">Emis par :</td>
								<td><xsl:value-of select="msg/trans/emis"/>&#160;</td>
                            </tr>
                            <tr>
								<td class="lib">Reçu par :</td>
								<td><xsl:value-of select="msg/trans/recu"/>&#160;</td>
							</tr>
                            <tr>
								<td>Instructions particulières :</td>
								<td><xsl:value-of select="msg/trans/instr"/>&#160;</td>
							</tr>
                        </table>
												<table class="pgh">
							<tr>
                                <th class="pgh" colspan="2">Informations Relevé SATER</th>
                            </tr>    
                            <tr>
								<td class="lib">Système de coordonnées :</td>
								<td><xsl:value-of select="msg/corps/sys"/>&#160;</td>
                            </tr>
                            <tr>
								<td class="lib">Datum :</td>
								<td><xsl:value-of select="msg/corps/datum"/>&#160;</td>
                            </tr>
                            <tr>
								<td class="lib">Coordonnées X :</td>
								<td><xsl:value-of select="msg/corps/coordx"/>&#160;</td>
							</tr>
                            <tr>
								<td>Coordonnées Y :</td>
								<td><xsl:value-of select="msg/corps/coordy"/>&#160;</td>
							</tr>
                            <tr>
								<td class="lib">Direction du relevé :</td>
								<td><xsl:value-of select="msg/corps/dir"/>&#160;</td>
                            </tr>
                            <tr>
								<td class="lib">Force du signal :</td>
								<td><xsl:value-of select="msg/corps/force"/>&#160;</td>
							</tr>
                            <tr>
								<td>Remarques :</td>
								<td><xsl:value-of select="msg/corps/txt"/>&#160;</td>
							</tr>
                        </table>
               </td>
            </tr>   
            <br/>

			</table>
            <div align="center"><input name="B1" onclick="imp1()" type="button" value="Imprimer Tout"/></div>
            <div align="center"><input name="B2" onclick="imp2()" type="button" value="Imprimer Message seul"/></div>
	</body>
</html>

</xsl:template>
</xsl:stylesheet>
