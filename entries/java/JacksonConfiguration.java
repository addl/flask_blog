package com.bms.mdc.skill.config;

import com.bms.mdc.skill.wrapper.Translatable;
import com.bms.mdc.skill.wrapper.TranslatableJsonSerializer;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.module.SimpleModule;
import commons.common.LanguageCacheHolder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;

@Configuration
public class JacksonConfiguration {

  @Autowired
  private LanguageCacheHolder storage;

  @Bean
  public ObjectMapper objectMapper() {
    ObjectMapper mapper = new ObjectMapper();
    SimpleModule simpleModule = new SimpleModule();
    simpleModule.addDeserializer(Translatable.class, new TranslatableJsonSerializer(storage));
    mapper.registerModule(simpleModule);
    return mapper;
  }

  @Bean
  public MappingJackson2HttpMessageConverter mappingJackson2HttpMessageConverter() {
    MappingJackson2HttpMessageConverter jsonConverter = new MappingJackson2HttpMessageConverter();
    jsonConverter.setObjectMapper(objectMapper());
    return jsonConverter;
  }

}
