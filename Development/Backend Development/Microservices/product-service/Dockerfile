FROM openjdk:11-jre-slim
WORKDIR /app
COPY target/product-service.jar app.jar
EXPOSE 8082
ENTRYPOINT ["java", "-jar", "app.jar"]
