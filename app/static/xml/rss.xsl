<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html"/>
    <xsl:template match="/">
        <div>
            <h2>
                <img>
                    <xsl:attribute name="src">
                        <xsl:value-of select="//channel/image/url"/>
                    </xsl:attribute>
                </img>
                <xsl:value-of select="//channel/title"/>
            </h2>
        </div>
        <br/>
        <xsl:for-each select="//item">
        <div class="card">
            <div class="card-header">
                <h4><xsl:value-of select="title"/></h4>
            </div>
            <div class="card-body" style="height: 120px; overflow: hidden;">
                <xsl:value-of select="description" disable-output-escaping="yes"/>
            </div>
            <div class="card-footer">
                <p>
                    <b>Publicada em: </b>
                    <xsl:value-of select="pubDate"/>
                </p>
                <a target="_blank">
                    <xsl:attribute name="href">
                        <xsl:value-of select="link"/>
                    </xsl:attribute>
                    Aceder à notícia completa.
                </a>
            </div>
        </div>
            <br/>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>