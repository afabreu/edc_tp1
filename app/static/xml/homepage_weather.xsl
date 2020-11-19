<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>
    <xsl:param name="rain_mode" select="current/precipitation/@mode"/>
    <xsl:variable name="rain_no" select='"no"'/>
    <xsl:template match="/">

        <div class="card rounded-lg mb-4" style="background-color: rgba(255, 255, 255, 0.5); max-width: 540px;">
            <div class="row no-gutters">
                <div class="col-md-4">
                    <img class="card-img">
                        <xsl:attribute name="src">http://openweathermap.org/img/wn/<xsl:value-of select="current/weather/@icon"/>@4x.png</xsl:attribute>
                    </img>
                </div>
                <div class="col-md-8">
                    <div class="card-body text-center">

                        <p class="card-text">
                            <h5 class="text-warning">
                                <i class="fas fa-temperature-high"></i>
                                <b><xsl:value-of select="current/temperature/@max"/>°C
                                </b>
                            </h5>
                            <h1><xsl:value-of select="current/temperature/@value"/>°C
                            </h1>
                            <h5 class="text-info">
                                <i class="fas fa-temperature-low"></i>
                                <b><xsl:value-of select="current/temperature/@min"/>°C
                                </b>
                            </h5>
                        </p>
                        <h5 class="card-title"><xsl:value-of select="current/city/@name"/></h5>
                    </div>
                </div>
            </div>
        </div>
</xsl:template>
</xsl:stylesheet>