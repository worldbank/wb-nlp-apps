<template>
  <div class="text-justify">
    <h1>{{ page_title }}</h1>
    <div>
      <br />
      <p>
        Metadata on each document is collected at the stage of web scraping. The
        metadata typically include the source, title, author, abstract if
        available, and the link to the PDF document. Some websites provide more
        information than others. Documents from the World Bank Documents and
        Reports provide significantly more metadata, accessible via API,
        including topic tagging (based on the World Bank’s specific taxonomy of
        topics, different from the topics we extract from LDA models),
        geographic coverage, document type and sub-type, and more. We cannot
        extract or generate similar information from other sources. We therefore
        limit the metadata elements to a core list. We augment these metadata
        elements by running data extraction scripts or NLP models. These
        metadata are processed, normalized, and stored in a MongoDB database.
        The metadata contained in the MongoDB database are then augmented and
        stored into Elasticsearch. Below is the list of available metadata
        fields.
      </p>
      <div class="meta-schema">
        <div class="sc-hKwCoD kOJmuK">
          <div>
            <div>
              <div class="sc-fmBDoT eNSIIY">
                <h5 class="sc-iqsfdx dONVW">Metadata Schema:</h5>
                <table class="sc-hGPAah kUYIEQ">
                  <tbody>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="id"
                      >
                        <span class="sc-ieebsP kMugIr"></span><span>id</span>
                        <div class="sc-TBWwm sc-jIkYaL gtdhUK fLAEHx">
                          required
                        </div>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >string</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Id)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>
                                Unique identifier for the document. Derived
                                identifiers such as <code>hex_id</code> will be
                                based on this.
                              </p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="hex_id"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>hex_id</span>
                        <div class="sc-TBWwm sc-jIkYaL gtdhUK fLAEHx">
                          required
                        </div>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >string</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Hex Id)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>
                                This id will be the basis for the
                                <code>int_id</code> that will be used in the
                                Milvus index.
                              </p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="int_id"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>int_id</span>
                        <div class="sc-TBWwm sc-jIkYaL gtdhUK fLAEHx">
                          required
                        </div>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >integer</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Int Id)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>
                                This will be the id derived from the
                                <code>hex_id</code> that will be used in the
                                Milvus index.
                              </p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="abstract"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>abstract</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >string</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Abstract)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>Abstract of the document.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="adm_region"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>adm_region</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                              >Array of </span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >strings</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Adm Region)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>
                                List of administrative regions. Example: Africa.
                              </p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="app_tag_jdc"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>app_tag_jdc</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >boolean</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (App Tag Jdc)
                            </span>
                          </div>
                          <div>
                            <span class="sc-faUofl lixDDm"> Default: </span>
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >false</span
                            >
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>
                                Tag associated with documents that belong to the
                                JDC collection.
                              </p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="author"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>author</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                              >Array of </span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >strings</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Author)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>List of author names.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="cleaning_config_id"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>cleaning_config_id</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >string</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Cleaning Config Id)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>
                                This corresponds to the configuration ID of the
                                cleaning pipeline that was used to generate the
                                cleaned file in the
                                <code>path_clean</code> field.
                              </p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="collection"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>collection</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >string</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Collection)
                            </span>
                          </div>
                          <div>
                            <div
                              class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG"
                            ></div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="corpus"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>corpus</span>
                        <div class="sc-TBWwm sc-jIkYaL gtdhUK fLAEHx">
                          required
                        </div>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >any</span
                            >
                          </div>
                          <div>
                            <span class="sc-faUofl lixDDm"> Enum:</span>
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"ADB"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"AFDB"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"ECLAC"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"EPDC"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"ESCAP"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"FAO"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"IADB"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"IIEP"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"IMF"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"OECD"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"UNECA"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"UNESCWA"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"UNHCR"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"UNIDO"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"UNODC"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"UNPD"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"WFP"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"WB"</span
                            >
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>The corpus id of the document source.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="country"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>country</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                              >Array of </span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >strings</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Country)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>
                                List of countries from the source repository, if
                                available.
                              </p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="date_published"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>date_published</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >string</span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj">
                              &lt;date&gt; </span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Date Published)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>Publication date of the document.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="der_acronyms"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>der_acronyms</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                              >Array of </span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >objects</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Der Acronyms)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>Extracted acronyms from the document.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="der_countries"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>der_countries</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >object</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Der Countries)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>
                                Frequency of extracted countries from the
                                document.
                              </p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="der_country"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>der_country</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                              >Array of </span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >strings</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Der Country)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>
                                List of unique country names extracted from the
                                document.
                              </p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="der_country_counts"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>der_country_counts</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >object</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Der Country Counts)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>
                                Frequency of extracted countries from the
                                document.
                              </p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="der_country_details"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>der_country_details</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                              >Array of </span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >any</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Der Country Details)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>
                                Detailed information on extracted countries from
                                the document.
                              </p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="der_country_groups"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>der_country_groups</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                              >Array of </span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >strings</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Der Country Groups)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>
                                List of country groups that the country
                                associated with the document belong to.
                              </p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="der_jdc_data"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>der_jdc_data</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                              >Array of </span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >objects</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Der Jdc Data)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>
                                List of objects corresponding to tags related to
                                JDC and their respective frequency of occurence
                                in the document.
                              </p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="der_jdc_tags"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>der_jdc_tags</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                              >Array of </span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >strings</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Der Jdc Tags)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>
                                List of tags found in <code>der_jdc_data</code>.
                              </p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="der_language_detected"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>der_language_detected</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >string</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Der Language Detected)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>Language detected in the document.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="der_language_score"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>der_language_score</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >number</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Der Language Score)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>Confidence score of the detected language.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="der_raw_token_count"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>der_raw_token_count</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >integer</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Der Raw Token Count)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>Count of raw tokens.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="der_regions"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>der_regions</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                              >Array of </span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >any</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (RegionTypes)
                            </span>
                          </div>
                          <div>
                            <span class="sc-faUofl lixDDm">Items Enum:</span>
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >""</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"East Asia &amp; Pacific"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"Europe &amp; Central Asia"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"Latin America &amp; Caribbean"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"Middle East &amp; North Africa"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"North America"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"South Asia"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"Sub-Saharan Africa"</span
                            >
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>
                                List of unique regions corresponding to
                                countries found in the document.
                              </p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="der_top_country"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>der_top_country</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >string</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Der Top Country)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>
                                Country with the highest frequency of mentions
                                in the document.
                              </p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="der_top_region"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>der_top_region</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >string</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Der Top Region)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>Region of the <code>der_top_country</code>.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="der_clean_token_count"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>der_clean_token_count</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >integer</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Der Clean Token Count)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>Count of cleaned tokens.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="digital_identifier"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>digital_identifier</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >string</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Digital Identifier)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>
                                Document digital identifier. For WB documents,
                                use the information from API; for other corpus,
                                use ISBN, or DOI, or other ID if available.
                              </p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="doc_type"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>doc_type</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                              >Array of </span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >strings</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Doc Type)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>
                                Document type as defined from the source
                                repository.
                              </p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="filename_original"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>filename_original</span>
                        <div class="sc-TBWwm sc-jIkYaL gtdhUK fLAEHx">
                          required
                        </div>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >string</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Filename Original)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>Filename of the document without path.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="geo_region"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>geo_region</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                              >Array of </span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >strings</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Geo Region)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>
                                List of geographic regions covered in the
                                document.
                              </p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="journal"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>journal</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >string</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Journal)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>Journal where the document is published.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="keywords"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>keywords</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                              >Array of </span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >strings</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Keywords)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>Keywords extracted from source API or page.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="language_src"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>language_src</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >string</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Language Src)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>
                                Language of the document specified in the source
                                repository.
                              </p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="last_update_date"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>last_update_date</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >string</span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj">
                              &lt;date-time&gt; </span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Last Update Date)
                            </span>
                          </div>
                          <div>
                            <span class="sc-faUofl lixDDm"> Default: </span>
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"2021-06-24T03:46:01.872859"</span
                            >
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>Date when the metadata was last updated.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="major_doc_type"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>major_doc_type</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                              >Array of </span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >any</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (MajorDocTypes)
                            </span>
                          </div>
                          <div>
                            <span class="sc-faUofl lixDDm">Items Enum:</span>
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >""</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"Board Documents"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"Project Documents"</span
                            >
                            <span class="sc-faUofl sc-eLwHGX lixDDm iSaGJa"
                              >"Publications and Reports"</span
                            >
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>Curated major document type.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="path_clean"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>path_clean</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >string</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Path Clean)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>Path to the cleaned text.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="path_original"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>path_original</span>
                        <div class="sc-TBWwm sc-jIkYaL gtdhUK fLAEHx">
                          required
                        </div>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >string</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Path Original)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>Path to the raw text.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="path_pdf_file"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>path_pdf_file</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >string</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Path Pdf File)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>Path of the scraped PDF file.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="project_id"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>project_id</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                              >Array of </span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >strings</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Project Id)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>Project id(s) associated with the document.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="title"
                      >
                        <span class="sc-ieebsP kMugIr"></span><span>title</span>
                        <div class="sc-TBWwm sc-jIkYaL gtdhUK fLAEHx">
                          required
                        </div>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >string</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Title)
                            </span>
                          </div>
                          <div>
                            <div
                              class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG"
                            ></div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="topics_src"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>topics_src</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                              >Array of </span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >strings</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Topics Src)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>Raw topics extracted from source.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="url_pdf"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>url_pdf</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >string</span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj">
                              &lt;uri&gt; </span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Url Pdf) </span
                            ><span>
                              <span class="sc-faUofl sc-kHOZQx lixDDm fyQLxh">
                                [ 1 .. 65536 ] characters
                              </span></span
                            >
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>URL to the PDF source.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="url_txt"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>url_txt</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >string</span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj">
                              &lt;uri&gt; </span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Url Txt) </span
                            ><span>
                              <span class="sc-faUofl sc-kHOZQx lixDDm fyQLxh">
                                [ 1 .. 65536 ] characters
                              </span></span
                            >
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>URL to the TXT source.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="volume"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>volume</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >string</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Volume)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>Volume of the journal.</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="wb_lending_instrument"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>wb_lending_instrument</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                              >Array of </span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >strings</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Wb Lending Instrument)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>World Bank metadata: lending instrument</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="wb_major_theme"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>wb_major_theme</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                              >Array of </span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >strings</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Wb Major Theme)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>World Bank metadata: major theme</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="wb_product_line"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>wb_product_line</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >string</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Wb Product Line)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>World Bank metadata: product line</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="wb_project_id"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>wb_project_id</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                              >Array of </span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >strings</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Wb Project Id)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>World Bank metadata: project id</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="wb_sector"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>wb_sector</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                              >Array of </span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >strings</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Wb Sector)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>World Bank metadata: sector</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="wb_subtopic_src"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>wb_subtopic_src</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                              >Array of </span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >strings</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Wb Subtopic Src)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>World Bank metadata: subtopic</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="wb_theme"
                      >
                        <span class="sc-ieebsP kMugIr"></span
                        ><span>wb_theme</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                              >Array of </span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >strings</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Wb Theme)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>World Bank metadata: theme</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr class="last undefined">
                      <td
                        class="sc-hBURRC sc-fFehDp bhpqyO ffwWXK"
                        kind="field"
                        title="year"
                      >
                        <span class="sc-ieebsP kMugIr"></span><span>year</span>
                      </td>
                      <td class="sc-bkkfTU irZUZr">
                        <div>
                          <div>
                            <span
                              class="sc-faUofl sc-GamvQ lixDDm grOQBI"
                            ></span
                            ><span class="sc-faUofl sc-fWCJfs lixDDm jAudhj"
                              >integer</span
                            ><span class="sc-faUofl sc-dvQbkV lixDDm ehRoAS">
                              (Year)
                            </span>
                          </div>
                          <div>
                            <div class="sc-iAKVOt sc-cNKpQo jRMZyJ bcRvbG">
                              <p>Year the document is published</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>

      <p>
        A separate Elasticsearch index is used to store the generated LDA topics for each document. We also use Milvus, a vector index, to store the vectors produced for each document by the different LDA topic models and word2vec models. All indexes use unique identifiers that can be used to connect to the metadata.
      </p><p>
An automated pipeline is implemented to automate the processing and generation of metadata and vectors for new documents.
</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Metadata",
  props: {
    page_title: String,
  },
  data: function () {
    return {
      date_now: new Date().toDateString(),
      corpus_size: 200000,
      org_count: 14,
      total_tokens: 1029000000,
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
div.sc-hKwCoD.kOJmuK {
  font-family: Roboto, sans-serif;
  font-size: 14px;
  font-weight: 400;
  line-height: 1.5em;
  color: rgb(51, 51, 51);
  text-align: left;
  -webkit-font-smoothing: antialiased;
  text-size-adjust: 100%;
  text-rendering: optimizespeed !important;
  width: 100%;
  padding: 20px;
  box-sizing: border-box;
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
  padding-right: 40px;
}

div.sc-fmBDoT.eNSIIY {
  font-family: Roboto, sans-serif;
  font-size: 14px;
  font-weight: 400;
  line-height: 1.5em;
  color: rgb(51, 51, 51);
  text-align: left;
  -webkit-font-smoothing: antialiased;
  text-size-adjust: 100%;
  text-rendering: optimizespeed !important;
  padding: 10px;
  box-sizing: border-box;
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
}

table {
  table-layout: fixed;
}
table.sc-hGPAah.kUYIEQ {
  font-family: Roboto, sans-serif;
  font-weight: 400;
  line-height: 1.5em;
  color: rgb(51, 51, 51);
  text-align: left;
  -webkit-font-smoothing: antialiased;
  text-size-adjust: 100%;
  text-rendering: optimizespeed !important;
  border-collapse: separate;
  border-radius: 3px;
  font-size: 14px;
  border-spacing: 0px;
  width: 100%;
  box-sizing: border-box;
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
}

td.sc-hBURRC.sc-fFehDp.bhpqyO.ffwWXK {
  font-weight: 400;
  color: rgb(51, 51, 51);
  text-align: left;
  -webkit-font-smoothing: antialiased;
  text-size-adjust: 100%;
  text-rendering: optimizespeed !important;
  border-collapse: separate;
  border-spacing: 0px;
  border-left: 1px solid rgb(124, 124, 187);
  position: relative;
  padding: 10px 10px 10px 0px;
  vertical-align: top;
  line-height: 20px;
  white-space: nowrap;
  font-size: 13px;
  font-family: Courier, monospace;
  box-sizing: border-box;
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
  border-left-width: 0px;
  background-position: left top;
  background-repeat: no-repeat;
  background-size: 1px 100%;
  background-image: linear-gradient(
    transparent 0%,
    transparent 22px,
    rgb(124, 124, 187) 22px,
    rgb(124, 124, 187) 100%
  );
}

span.sc-ieebsP.kMugIr {
  font-weight: 400;
  text-align: left;
  -webkit-font-smoothing: antialiased;
  text-size-adjust: 100%;
  text-rendering: optimizespeed !important;
  border-collapse: separate;
  border-spacing: 0px;
  line-height: 20px;
  white-space: nowrap;
  font-size: 13px;
  color: rgb(124, 124, 187);
  font-family: Courier, monospace;
  margin-right: 10px;
  box-sizing: border-box;
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
}

div.sc-TBWwm.sc-jIkYaL.gtdhUK.fLAEHx {
  text-align: left;
  -webkit-font-smoothing: antialiased;
  text-size-adjust: 100%;
  text-rendering: optimizespeed !important;
  border-collapse: separate;
  border-spacing: 0px;
  white-space: nowrap;
  font-family: Courier, monospace;
  vertical-align: middle;
  color: rgb(212, 31, 28);
  font-size: 0.9em;
  font-weight: normal;
  margin-left: 20px;
  line-height: 1;
  box-sizing: border-box;
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
}

td.sc-bkkfTU.irZUZr {
  font-family: Roboto, sans-serif;
  font-weight: 400;
  line-height: 1.5em;
  color: rgb(51, 51, 51);
  text-align: left;
  -webkit-font-smoothing: antialiased;
  text-size-adjust: 100%;
  text-rendering: optimizespeed !important;
  border-collapse: separate;
  font-size: 14px;
  border-spacing: 0px;
  border-bottom: 1px solid rgb(159, 180, 190);
  padding: 10px 0px;
  width: 75%;
  box-sizing: border-box;
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
}

span.sc-faUofl.sc-GamvQ.lixDDm.grOQBI {
  font-family: Roboto, sans-serif;
  font-weight: 400;
  text-align: left;
  -webkit-font-smoothing: antialiased;
  text-size-adjust: 100%;
  text-rendering: optimizespeed !important;
  border-collapse: separate;
  border-spacing: 0px;
  vertical-align: middle;
  font-size: 13px;
  line-height: 20px;
  color: rgba(102, 102, 102, 0.9);
  box-sizing: border-box;
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
}

span.sc-faUofl.sc-fWCJfs.lixDDm.jAudhj {
  font-family: Roboto, sans-serif;
  font-weight: 400;
  text-align: left;
  -webkit-font-smoothing: antialiased;
  text-size-adjust: 100%;
  text-rendering: optimizespeed !important;
  border-collapse: separate;
  border-spacing: 0px;
  vertical-align: middle;
  font-size: 13px;
  line-height: 20px;
  color: rgb(102, 102, 102);
  box-sizing: border-box;
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
}

span.sc-faUofl.sc-dvQbkV.lixDDm.ehRoAS {
  font-family: Roboto, sans-serif;
  font-weight: 400;
  text-align: left;
  -webkit-font-smoothing: antialiased;
  text-size-adjust: 100%;
  text-rendering: optimizespeed !important;
  border-collapse: separate;
  border-spacing: 0px;
  vertical-align: middle;
  font-size: 13px;
  line-height: 20px;
  color: rgb(102, 102, 102);
  word-break: break-word;
  box-sizing: border-box;
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
}

div.sc-iAKVOt.sc-cNKpQo.jRMZyJ.bcRvbG {
  color: rgb(51, 51, 51);
  text-align: left;
  -webkit-font-smoothing: antialiased;
  text-size-adjust: 100%;
  text-rendering: optimizespeed !important;
  border-collapse: separate;
  font-size: 14px;
  border-spacing: 0px;
  font-family: Roboto, sans-serif;
  font-weight: 400;
  line-height: 1.5em;
  box-sizing: border-box;
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
}

.kMugIr::before {
  content: "";
  display: inline-block;
  vertical-align: middle;
  width: 10px;
  height: 1px;
  background: rgb(124, 124, 187);
}

.kMugIr::after {
  content: "";
  display: inline-block;
  vertical-align: middle;
  width: 1px;
  background: rgb(124, 124, 187);
  height: 7px;
}

tr {
  font-family: Roboto, sans-serif;
  font-weight: 400;
  line-height: 1.5em;
  color: rgb(51, 51, 51);
  text-align: left;
  -webkit-font-smoothing: antialiased;
  text-size-adjust: 100%;
  text-rendering: optimizespeed !important;
  border-collapse: separate;
  font-size: 14px;
  border-spacing: 0px;
  box-sizing: border-box;
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
}

span.sc-faUofl.lixDDm {
  font-family: Roboto, sans-serif;
  font-weight: 400;
  color: rgb(51, 51, 51);
  text-align: left;
  -webkit-font-smoothing: antialiased;
  text-size-adjust: 100%;
  text-rendering: optimizespeed !important;
  border-collapse: separate;
  border-spacing: 0px;
  vertical-align: middle;
  font-size: 13px;
  line-height: 20px;
  box-sizing: border-box;
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
}

span.sc-faUofl.sc-eLwHGX.lixDDm.iSaGJa {
  display: inline-block;
  font-weight: 400;
  text-align: left;
  -webkit-font-smoothing: antialiased;
  text-size-adjust: 100%;
  text-rendering: optimizespeed !important;
  border-collapse: separate;
  border-spacing: 0px;
  vertical-align: middle;
  font-size: 13px;
  line-height: 20px;
  border-radius: 2px;
  background-color: rgba(51, 51, 51, 0.05);
  color: rgba(51, 51, 51, 0.9);
  padding: 0px 5px;
  border: 1px solid rgba(51, 51, 51, 0.1);
  font-family: Courier, monospace;
  box-sizing: border-box;
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
  margin: 3px;
}

td.sc-hBURRC.sc-fFehDp bhpqyO.ffwWXK {
  font-weight: 400;
  color: rgb(51, 51, 51);
  text-align: left;
  -webkit-font-smoothing: antialiased;
  text-size-adjust: 100%;
  text-rendering: optimizespeed !important;
  border-collapse: separate;
  border-spacing: 0px;
  border-left: 1px solid rgb(124, 124, 187);
  position: relative;
  padding: 10px 10px 10px 0px;
  vertical-align: top;
  line-height: 20px;
  white-space: nowrap;
  font-size: 13px;
  font-family: Courier, monospace;
  box-sizing: border-box;
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
}

span.sc-faUofl.sc-kHOZQx.lixDDm.fyQLxh {
  font-weight: 400;
  text-align: left;
  -webkit-font-smoothing: antialiased;
  text-size-adjust: 100%;
  text-rendering: optimizespeed !important;
  border-collapse: separate;
  border-spacing: 0px;
  vertical-align: middle;
  font-size: 13px;
  line-height: 20px;
  border-radius: 2px;
  background-color: rgba(104, 104, 207, 0.05);
  color: rgba(50, 50, 159, 0.9);
  margin: 0px 5px;
  padding: 0px 5px;
  border: 1px solid rgba(50, 50, 159, 0.1);
  font-family: Courier, monospace;
  box-sizing: border-box;
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
}
</style>
