# 訂閱按鈕按下後的付款流程

```mermaid
sequenceDiagram
    autonumber
    
    participant ui as Web Browser
    participant api as Platform API
    participant pg as Payment Gateway
    participant stripe as Strip Service

    Note over ui,stripe: ui 以及 api 並不應該直接操作 Stripe API，也不該知道 Stripe 的存在
    ui ->> api: 選擇不同方案訂閱按鈕按下後 <br> 打 API 到後端
    api ->> ui: 回傳 PG Callback Endpoint & <br>subscription 相關資訊 ( ex: Pricing Plan's lookup key )

    ui ->>+ pg: *SyncPost* with Transaction ID with Subscription Information
    Note right of pg: 記下 transaction id  redis 中
    pg ->> stripe: 使用 Checkout.session.create 建立 Stripe Host Checkout 畫面
    stripe ->> pg: 回傳 checkout.url

    PAR pg to ui
        pg ->>- ui: pg 回傳 checkout.url
    and pg to api
        pg ->> api: pg 以 Domain Event 通知 API
    end

    ui -->>+ stripe: redirect to Stripe 付款

    PAR 使用者付款後的結果
        alt  成功
            stripe -->> ui: redirect 至成功畫面
        else 失敗
            stripe -->>- ui: redirect 至取消畫面
        end
    and 
        stripe ->> pg: Stripe 通過 Webhook 非同步通知 Payment Gateway
        Note right of pg: 去除 redis 中的 transaction id
    end
```

# 接收 Stripe Webhook 事件

```mermaid
sequenceDiagram
    autonumber
    
    participant ui as Web Browser
    participant api as Platform API
    participant pg as Payment Gateway
    participant stripe as Strip Service

    Note over ui,stripe: ui 以及 api 並不應該直接操作 Stripe API，也不該知道 Stripe 的存在

    stripe ->> pg: 使用 Webhook 通知 Payment Gateway 事件發生
    PAR
        pg ->> pg: 處理相關商業邏輯
    AND
        pg -->> api: 以 Domain Event 的方式通知 Platform ( Pare-Eventing )
    END
```


# 取得 Billing & Payment History 流程

```mermaid
sequenceDiagram
    autonumber
    
    participant ui as Web Browser
    participant api as Platform API
    participant pg as Payment Gateway
    participant stripe as Strip Service

    Note over ui,stripe: ui 以及 api 並不應該直接操作 Stripe API，也不該知道 Stripe 的存在
    ui ->> api: 進入頁面後，打API到後端
    api ->> ui: 回傳 PG Callback Endpoint & <br> Custom 相關資訊 ( ex: Custom ID )

    ui ->>+ pg: *SyncGet* with Custom ID & 偏移量 & Subscription ID 
    pg ->> stripe: 使用 stripe.Invoice.list
    stripe ->> pg: 回傳 Invoice 列表
    pg ->>- ui: pg 回傳 Invoice 列表
```


# Payment Gateway 狀態圖

```mermaid
stateDiagram-v2

    [*] --> SubscriptionCreated: "customer.subscription.created"

    SubscriptionCreated --> InvoiceCreated: "invoice.created"

    InvoiceCreated --> PaymentFailed: "invoice.payment_failed"
    InvoiceCreated --> PaymentPaid: "invoice.payment_succeeded"

    PaymentFailed --> PaymentPaid: "invoice.payment_succeeded"
    PaymentFailed --> PaymentFailed: retry and failed again <br>"invoice.payment_failed"

    % 再次訂閱
    PaymentPaid --> InvoiceCreated : 下一週期"invoice.created"

    PaymentPaid --> SubscriptionDeleted : "customer.subscription.deleted"
    SubscriptionDeleted --> [*]
```

RAPD Events:  
SubscriptionCreated  
InvoiceCreated  
PaymentPaid  
PaymentFailed  
SubscriptionDeleted  

Stripe Events:
customer.subscrption.created
invoice.created
invoice.payment_failed
invoice.payment_succeeded
customer.subscription.deleted


---

# UML Class Diagram

```mermaid

classDiagram

    direction TB

    %%%%%%% 關係定義

    PaymentService <|-- StripePaymentService

    StateBase <|-- SubscriptionCreatedState
    StateBase <|-- InvoiceCreatedState
    StateBase <|-- PaymentFailedState
    StateBase <|-- PaymentPaidState
    StateBase <|-- SubscriptionDeletedState


    StateTransitEvent <|-- CustomerSubscriptionCreatedEvent
    StateTransitEvent <|-- InvoiceCreatedEvent
    StateTransitEvent <|-- ChargeSucceededEvent
    StateTransitEvent <|-- InvoicePaymentFailedEvent
    StateTransitEvent <|-- InvoicePaymentSucceededEvent


    EventHandler <|-- CustomerSubscriptionCreatedStrategy
    EventHandler <|-- InvoiceCreatedStrategy
    EventHandler <|-- ChargeSucceededStrategy
    EventHandler <|-- InvoicePaymentFailedStrategy
    EventHandler <|-- InvoicePaymentSucceededStrategy

    EventHandler o-- DababaseService
    EventHandler o-- PareEventingService
    EventHandler o-- JWTIssuer
    EventHandler *-- CloudEvent
    
    StripePaymentService o-- DababaseService
    StripePaymentService o-- StateRegistry
    StateRegistry *-- StateBase
    StateBase *-- EventHandler
    StateBase *-- StateTransitEvent
    


    %%%%%%% 物件定義
    
    class PaymentService {
        <<interface>>
        +GetCustomer()
        +CreateCustomer()
        +GetSubscription()
        +CreateSubscription()
        +GetInvoice()
        +GetInvoicesList()
        +CreateInvoice()
    }

    class StripePaymentService { }

    class StateRegistry {
        -handled_states
        +__getitem__()
        +__setitem__()
    }


    %% Event Handler： 封裝了怎麼處理該次 Event 的發生
    class EventHandler { 
        <<interface>>
        -handled_states
        +handle_event(event: Type~EventBase~)
    }
    class CustomerSubscriptionCreatedStrategy { }
    class InvoiceCreatedStrategy { }
    class ChargeSucceededStrategy { }
    class InvoicePaymentFailedStrategy { }
    class InvoicePaymentSucceededStrategy { }


    class StateBase {
        <<interface>>
        +from_event(event: dict) Self
    }
    class SubscriptionCreatedState { }
    class InvoiceCreatedState { }
    class PaymentFailedState { }
    class PaymentPaidState { }
    class SubscriptionDeletedState { }


    %% 這些都是 Stripe Event Dataclass，會導致訂閱的狀態轉換
    class StateTransitEvent {
        <<Abstract>>
        +from_event(raw_event: dict)
    }
    class CustomerSubscriptionCreatedEvent { }
    class InvoiceCreatedEvent { }
    class ChargeSucceededEvent { }
    class InvoicePaymentFailedEvent { }
    class InvoicePaymentSucceededEvent { }

    %% 用於資料庫存放的字串
    class StateEnum {
        <<Enumeration>>
        SubscriptionCreated
        InvoiceCreated
        PaymentFailed
        PaymentPaid
        SubscriptionDeleted
    }


    %% 原本就存在的物件
    %% Container 中的 SharedContainer 中的 database
    class DababaseService { }
    class PareEventingService { }
    class CloudEvent { }
    class JWTIssuer { }

```
<!-- 
    class EventDispatcher {
        + handlers

        +register_handler(event, handler: Type~EventHandler~)
        +dispatch_event(event)
    } -->

---

```mermai
sequenceDiagram
    participant web as Web Browser
    participant blog as Blog Service
    participant account as Account Service
    participant mail as Mail Service
    participant db as Storage


    Note over web,db: The user must be logged in to submit blog posts
    web->>+account: Logs in using credentials
    account->>db: Query stored accounts
    db->>account: Respond with query result

    alt Credentials not found
        account->>web: Invalid credentials
    else Credentials found
        account->>-web: Successfully logged in

        Note over web,db: When the user is authenticated, they can now submit new posts
        web->>+blog: Submit new post
        blog->>db: Store post data

        par Notifications
            blog--)mail: Send mail to blog subscribers
            blog--)db: Store in-site notifications
        and Response
            blog-->>-web: Successfully posted
        end
    end
```



---

之後要 publish 到 pare-eventing 的時候要放 token
因此要嘛用前端帶的 access_token 要嘛用 jwt_issuerl.issue 產的 token


這邊可以看到 jwt_issuer.issue 發 token 的方法
payload 裡面目前隨便放也都可以
/Users/henryli/coding/pentiumnetwork/mavis-auto-platform/mavis-auto/modules/events/api/endpoint.py

這邊定義了 jwt_issuer 被 container provider 實體化的地方
/Users/henryli/coding/pentiumnetwork/mavis-auto-platform/mavis-auto/application/containers/shared_mod.py

這邊定義了 pare_eventing_svc.publish 的方法
/Users/henryli/coding/pentiumnetwork/mavis-auto-platform/mavis-auto/modules/events/domain/infra/pare_eventing_service.py