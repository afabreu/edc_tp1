<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>
    <xsl:param name="rain_mode" select="current/precipitation/@mode"/>
    <xsl:variable name="rain_no" select='"no"' />
    <xsl:template match="/">
        <div class="row">
            <div class="col-sm-2">
                <img>
                    <xsl:attribute name="src">http://openweathermap.org/img/wn/<xsl:value-of select="current/weather/@icon"/>@4x.png</xsl:attribute>
                </img>
            </div>
            <div class="col-sm-2">
                <br/>
                <h5 class="text-warning"> <i class="fas fa-temperature-high"></i> <b> <xsl:value-of select="current/temperature/@max"/>°C</b> </h5>
                <h1><xsl:value-of select="current/temperature/@value"/>°C</h1>
                <h5 class="text-info"> <i class="fas fa-temperature-low"></i> <b> <xsl:value-of select="current/temperature/@min"/>°C</b></h5>
            </div>
        </div>
        <table class="table">
            <tbody>
                <tr>
                    <th scope="row">Temperatura</th>
                    <td><xsl:value-of select="current/temperature/@value"/>°C (min:<xsl:value-of select="current/temperature/@min"/>°C - max:<xsl:value-of select="current/temperature/@max"/> °C )</td>
                </tr>
                <tr>
                    <th scope="row">Sensação Térmica</th>
                    <td><xsl:value-of select="current/feels_like/@value"/>°C</td>
                </tr>
                <tr>
                    <th scope="row">Precipitação</th>
                    <xsl:choose>
                        <xsl:when test='$rain_no = $rain_mode'>
                            <td>Neste momento não está a chover</td>
                        </xsl:when>
                        <xsl:otherwise>
                            <td><xsl:value-of select="current/precipitation/@value"/> %</td>
                        </xsl:otherwise>
                    </xsl:choose>
                </tr>
                <tr>
                    <th scope="row">Humidade</th>
                    <td><xsl:value-of select="current/humidity/@value"/> %</td>
                </tr>
                <tr>
                    <th scope="row">Pressão</th>
                    <td><xsl:value-of select="current/pressure/@value"/> hPa</td>
                </tr>
                <tr>
                    <th scope="row">Velocidade Vento</th>
                    <td><xsl:value-of select="current/wind/speed/@value"/> m/s -- <xsl:value-of select="current/wind/speed/@name"/></td>
                </tr>
                <xsl:choose>
                    <xsl:when test="current/wind/gusts/@*">
                        <tr>
                            <th scope="row">Rajadas Vento</th>
                            <td><xsl:value-of select="current/wind/gusts/@value"/> m/s</td>
                        </tr>
                    </xsl:when>
                    <xsl:otherwise></xsl:otherwise>
                </xsl:choose>
                <xsl:choose>
                    <xsl:when test="current/wind/direction/@*">
                        <tr>
                            <th scope="row">Direção Vento</th>
                            <td><xsl:value-of select="current/wind/direction/@name"/></td>
                        </tr>
                    </xsl:when>
                    <xsl:otherwise></xsl:otherwise>
                </xsl:choose>

                <tr>
                    <th scope="row">Nuvens</th>
                    <td><xsl:value-of select="current/clouds/@value"/> % -- <xsl:value-of select="current/clouds/@name"/></td>
                </tr>
                <tr>
                    <th scope="row">Visibilidade</th>
                    <td><xsl:value-of select="current/visibility/@value"/></td>
                </tr>
            </tbody>
        </table>
    </xsl:template>
</xsl:stylesheet>