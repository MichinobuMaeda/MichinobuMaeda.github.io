Google App Engine で Spring Framework
=====

Update: 2010-10-05


参考にした本は「新人プログラマのための Google App Engine クラウド・アプリケーション開発講座」（掌田津耶乃 ISBN978-4-89977-248-4）です。そこそこ分量のある本なのですが、 Java で Google 提供の Ajax フレームワークを使わずにとなると、実際に使うのはほんの一部です。この著者の文章は読みやすくて、応用の利く説明の仕方になっているので Python の入門書としても使えるんじゃないかと思うけど、それはまた後日。


さて、この本の Java の章（の最初の方だけ）をざっと見て理解したのは Google App Engine の Java 向けの環境ってのは、要するに、標準の Servlet API が使える Web サーバ だということ。もしやと思いつつ Spring Framework 3.0 を突っ込んでみたら動きましたよ。 Struts あたりもだいじょうぶなんじゃないかな。

そういうわけで、週末から先ほどまでの間に書いてみた、ほんの少しのプログラムは、

*   Interceptor で、つまり、ビジネスロジックが動く前の処理として Google が提供するユーザ管理の仕組みで認証する。
*   JSP のページを 1ページだけ表示する。

という簡単なものです。とはいえ、簡単なことが簡単にできるっていうのはなかなかないことです。以下、そのあらまし。


環境の準備については本やオンラインドキュメントを見ればわかるのでここには書きません。最新の情報を一つだけ。 Eclipse 3.6 Helios に対応したプラグインが出てます。 http://code.google.com/intl/en/appengine/downloads.html

Google が提供するユーザ管理の仕組みについてはこちら http://code.google.com/intl/en/appengine/docs/java/gettingstarted/usingusers.html と、こちら http://code.google.com/intl/en/appengine/docs/java/users/ をどうぞ。



Spring Framework 3.0 の Interceptor の設定はリファレンスの “15.4 Handler mappings” をどうぞ。

Eclipse から起動するテストサーバはこんなログイン画面を出してくれます。

![](https://lh3.googleusercontent.com/_8rt3l_eFSnQ/TTw5Ygl8ZkI/AAAAAAAABqg/C9zeSS9mFos/gae001.png)

アプリケーションの ID は zippyzipjp です。

appengine-web.xml は次の行だけ書き換えます。

```
    <application>zippyzipjp</application>
```

web.xml は基本的なことだけ。

```
  <servlet>
    <servlet-name>zippyzipjp</servlet-name>
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    <load-on-startup>1</load-on-startup>
  </servlet>
  <servlet-mapping>
    <servlet-name>zippyzipjp</servlet-name>
    <url-pattern>/zippyzipjp/*</url-pattern>
  </servlet-mapping>
  <welcome-file-list>
    <welcome-file>index.html</welcome-file>
  </welcome-file-list>`
```


zippyzipjp-servlet.xml には、

*   Controller クラスの場所
*   View の場所と拡張子
*   Interceptor のクラス名

を書きました。


```
<!--
  - The controllers are autodetected POJOs labeled with the @Controller annotation.
-->
<context:component-scan base-package="jp.zippyzip.web"/>
  <!--
    - This bean configures the 'prefix' and 'suffix' properties of
    - InternalResourceViewResolver, which resolves logical view names
    - returned by Controllers. For example, a logical view name of "vets"
    - will be mapped to "/WEB-INF/jsp/vets.jsp".
  -->
  <bean class="org.springframework.web.servlet.view.InternalResourceViewResolver"
    p:prefix="/WEB-INF/jsp/" p:suffix=".jsp" p:order="2"/>
  <bean id="handlerMapping"
    class="org.springframework.web.servlet.mvc.annotation.DefaultAnnotationHandlerMapping">
    <property name="interceptors">
      <bean class="jp.zippyzip.web.GoogleUserAuthInterceptor"/>
    </property>
  </bean>
```

Java の実装はこんな感じで。


```
package jp.zippyzip.web;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.servlet.ModelAndView;

@Controller
@RequestMapping("/")
public class DefaultController {

    @RequestMapping(method = RequestMethod.GET)
    public ModelAndView welcomeHandler() {

        ModelAndView mav = new ModelAndView();
        mav.setViewName("default");
        return mav;
    }
}
```

```
package jp.zippyzip.web;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.web.servlet.handler.HandlerInterceptorAdapter;
import com.google.appengine.api.users.UserService;
import com.google.appengine.api.users.UserServiceFactory;

public class GoogleUserAuthInterceptor extends HandlerInterceptorAdapter {

    @Override
    public boolean preHandle(HttpServletRequest request,
            HttpServletResponse response, Object handler) throws Exception {
        UserService userService = UserServiceFactory.getUserService();
        if (!userService.isUserLoggedIn()) {
            response.sendRedirect(userService.createLoginURL(
            request.getRequestURI()));
            return false;
        }
        return true;
    }
}
```
