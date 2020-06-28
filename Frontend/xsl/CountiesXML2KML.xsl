<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <kml xmlns="http://www.opengis.net/kml/2.2">
            <Document id="root_doc">
                <Folder>
                    <name>mapschema_92_16.layertable_258_16</name>
                    <xsl:for-each select="Request/data/countries/country">
                        <Placemark>
                            <name>
                                <xsl:value-of select="./@countryname"/>
                            </name>
                            <Style>
                                <LineStyle>
                                    <color>ffffff</color>
                                    <width>1.0</width>
                                </LineStyle>
                                <PolyStyle>
                                    <fill>0</fill>
                                </PolyStyle>
                            </Style>
                            <MultiGeometry>
                                <Polygon>
                                    <innerBoundaryIs>
                                        <LinearRing>
                                            <coordinates>
                                                <xsl:for-each select="./point">
                                                    <xsl:value-of select="longitude"/>,<xsl:value-of select="latitude"/> &#160;
                                                </xsl:for-each>
                                            </coordinates>
                                        </LinearRing>
                                    </innerBoundaryIs>
                                </Polygon>
                            </MultiGeometry>
                        </Placemark>
                    </xsl:for-each>


                </Folder>
            </Document>
        </kml>
    </xsl:template>
</xsl:stylesheet>