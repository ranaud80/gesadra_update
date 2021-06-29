<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format">
	<!-- 
	style-sheet de présentation des messages BILAMB
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
                                <th class="pgh" colspan="2">Message BILAMB</th>
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
							<tr>
								<td class="lib">Objet</td>
								<td><xsl:value-of select="msg/corps/obj"/>&#160;</td>
							</tr>    
							<tr>
								<td class="lib">Localisation</td>
								<td><xsl:value-of select="msg/corps/local"/>&#160;</td>
							</tr>    
							<tr>
								<td class="lib" valign="top">Message</td>
                                <td >
									<xsl:for-each select="msg/corps/txt">
										<xsl:value-of select="."/><br/>
									</xsl:for-each>
                                </td>
							</tr>    
						</table>
						<br/>
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
                                        Message BILAMB
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
