@@@ aws-big-picture | Walk me through a typical secure web architecture on AWS. | devops | aws,cloud,architecture,vpc | qa | AWS
"From the outside in: Route 53 for DNS, CloudFront as CDN with AWS WAF, then an Application Load Balancer in **public subnets**. The application runs in **private subnets** on ECS, EKS or EC2 in an Auto Scaling group, spread across at least two availability zones. Databases such as RDS and ElastiCache sit in separate private data subnets.

Outbound internet from private subnets goes through a NAT gateway, one per AZ for availability. Traffic to S3 or DynamoDB uses a VPC gateway endpoint so it never touches the internet and costs no NAT fees.

Security layers: security groups chained by reference (ALB → app → database), IAM roles for workloads instead of keys, KMS encryption at rest, Secrets Manager for credentials, CloudTrail and CloudWatch for audit and monitoring. Single points of failure to call out: a single NAT gateway, a single-AZ database, or one region if the business needs regional DR."

Tham khảo thêm: [Cloud Architecture - The Big Picture](https://minhnhat97kg.github.io/docsify/content/cloud-architecture-the-big-picture/vi.md), [VPC & Subnet Architecture](https://minhnhat97kg.github.io/docsify/content/devops-vpc-virtual-private-cloud-subnet-architecture/vi.md)

@@@ aws-sg-nacl | Security Group vs Network ACL vs WAF? | devops | aws,security,networking,vpc | qa | AWS
"**Security groups** attach to network interfaces, allow rules only, and are **stateful**: return traffic is allowed automatically. **NACLs** apply to a subnet, have ordered allow and deny rules, and are **stateless**, so you must also allow return traffic on ephemeral ports 1024–65535, a common mistake.

A packet must pass both: if the NACL allows it but the security group doesn't, the instance never sees it. To block one attacking IP, use a NACL deny rule or WAF, since security groups can't deny. In practice most teams leave NACLs at default and do everything with security groups, because they're stateful and can reference other groups.

**WAF** works at layer 7 on CloudFront, ALB or API Gateway: SQL injection and XSS patterns, rate-based rules, geo-blocking, bot control. It sees decrypted HTTPS because it runs where TLS terminates. It can't protect against an attacker already inside the VPC."

Tham khảo thêm: [Security Groups vs NACL](https://minhnhat97kg.github.io/docsify/content/aws-security-groups-vs-nacl/vi.md), [AWS WAF](https://minhnhat97kg.github.io/docsify/content/aws-waf-web-application-firewall/vi.md)

@@@ aws-iam | How do IAM roles and policies work? How do you apply least privilege? | devops | aws,iam,security | qa | AWS
"A **user** is a long-lived identity with credentials; a **role** is assumed temporarily and gives short-lived credentials through STS. Workloads always use roles: an EC2 instance profile, an ECS task role, or IRSA or EKS Pod Identity for Kubernetes pods. No access keys in code.

A policy lists allowed or denied actions on resources, with optional conditions. Evaluation: everything is implicitly denied, an explicit allow grants access, and an explicit deny always wins. Permission boundaries and organization SCPs cap the maximum a role can ever get.

Least privilege in practice: start narrow, scope resources by ARN, use IAM Access Analyzer to trim unused permissions, and manage policies in Terraform. Developers reach production through SSO and short-lived role sessions, ideally read-only by default with audited break-glass access.

If a key leaks to GitHub: deactivate and delete it immediately, check CloudTrail for what it was used for, rotate anything it could reach, then fix the process with secret scanning."

Tham khảo thêm: [IAM Roles & Policies](https://minhnhat97kg.github.io/docsify/content/aws-iam-roles-policies-least-privilege/vi.md)

@@@ aws-kms | What is envelope encryption with KMS? | devops | aws,kms,encryption,security | qa | AWS
"KMS keys never leave the KMS hardware, and `Encrypt` only accepts up to 4 KB, so you don't send your data to KMS. Instead:

1. Call `GenerateDataKey`: KMS returns a plaintext data key and the same key encrypted under your KMS key.
2. Encrypt the data locally with the plaintext key using AES-GCM, then discard the plaintext key from memory.
3. Store the encrypted data key next to the ciphertext.
4. To decrypt, send the encrypted data key to KMS `Decrypt`, then decrypt locally.

Benefits: large data never crosses the network to KMS, each object can have its own key, access to decryption is controlled and audited through IAM and CloudTrail. With automatic rotation, KMS keeps old key material to decrypt old data keys, so you don't re-encrypt the database. Multi-region keys let you decrypt in a DR region."

Tham khảo thêm: [AWS - KMS & Envelope Encryption](https://minhnhat97kg.github.io/docsify/content/aws-aws-kms-envelope-encryption/vi.md)

@@@ aws-secrets | Secrets Manager vs Parameter Store, and how does rotation work? | devops | aws,security,secrets | qa | AWS
"Secrets Manager stores secrets encrypted with KMS and can rotate them automatically with a Lambda, with built-in support for RDS. Parameter Store is cheaper, and free for standard parameters, but has no built-in rotation. I use Secrets Manager for database credentials and API keys, and Parameter Store for ordinary configuration.

Rotation uses two versions, so the application doesn't break: the new password is created and set in the database while the old one stays valid, then the 'current' label moves. Existing connections keep working because databases check the password only when a connection opens; new connections pick up the new value.

In the application I cache the secret with a TTL rather than calling the API on every request, and on an authentication error I refresh the cache and retry once. Access is restricted per service through IAM, and every read is in CloudTrail."

Tham khảo thêm: [AWS - Secrets Manager & Automated Rotation](https://minhnhat97kg.github.io/docsify/content/aws-aws-secrets-manager-automated-rotation/vi.md)

@@@ aws-rds | RDS Multi-AZ vs read replicas? | devops | aws,database,high-availability | qa | AWS
"They solve different problems.

**Multi-AZ** is for **availability**: a standby in another AZ with synchronous replication. You can't read from the classic standby. On failure, RDS fails over by switching DNS, typically within a minute or two. Writes are slightly slower because each commit waits for the standby.

**Read replicas** are for **read scaling**: asynchronous copies you query directly, possibly in other regions. They have replication lag, so a user may not see their own write; read-your-writes paths go to the primary.

Write scaling needs other tools: a bigger instance, batching, caching, queues, or sharding. **Aurora** separates compute from a storage layer replicated six ways across three AZs; replicas share storage, so lag is usually tens of milliseconds and failover is faster."

Tham khảo thêm: [RDS Multi-AZ vs Read Replicas](https://minhnhat97kg.github.io/docsify/content/aws-aws-rds-multi-az-vs-read-replicas/vi.md)

@@@ aws-s3 | What should a backend engineer know about S3? | devops | aws,s3,storage | qa | AWS
"S3 is object storage: you replace whole objects, not edit blocks like a disk. Since December 2020 it's **strongly consistent** for reads after writes and lists.

Cost: storage classes from Standard to Infrequent Access to Glacier, with lifecycle rules to move or expire objects; Intelligent-Tiering when access patterns are unknown.

Patterns:

- **Presigned URLs** so clients upload and download directly, without streaming files through the API servers.
- **Multipart upload** for large files, roughly over 100 MB: parallel parts, retry per part.
- **Versioning plus Object Lock** to recover from accidental deletes or ransomware.
- Static websites: S3 behind CloudFront with origin access control, so the bucket stays private.

Security: block public access at the account level, encrypt with SSE-KMS, and grant access through bucket policies and IAM roles."

Tham khảo thêm: [S3 - Object Storage, Lifecycle & Consistency](https://minhnhat97kg.github.io/docsify/content/s3-simple-storage-service-object-storage-lifecycle-consistency/vi.md)

@@@ aws-lambda | When would you use AWS Lambda, and what are its limits? | devops | aws,serverless,lambda | qa | AWS
"Lambda runs functions on events with no servers to manage and per-request billing. It fits glue work: processing files after an S3 upload, consuming SQS or EventBridge events, scheduled jobs, and low or spiky-traffic APIs.

Limits: maximum 15 minutes per invocation, memory up to 10 GB, CPU tied to memory, no long-lived connections, and **cold starts** when a new environment starts. Go has small cold starts; Java's are larger, which SnapStart or provisioned concurrency mitigate.

Practical points: initialize clients outside the handler so warm invocations reuse them; use RDS Proxy because many concurrent functions can exhaust database connections; make handlers idempotent because events can be delivered more than once; and attach a dead-letter queue or on-failure destination for failed async events. For long or steady workloads, containers on ECS or Kubernetes are usually cheaper."

Tham khảo thêm: [DevOps - AWS Lambda](https://minhnhat97kg.github.io/docsify/content/devops-aws-lambda-serverless-compute/vi.md)

@@@ aws-autoscaling | How does EC2 Auto Scaling work? | devops | aws,ec2,autoscaling,high-availability | qa | AWS
"Three parts: a **launch template** describing the instance, an **Auto Scaling group** with minimum, desired and maximum counts across AZs, and **scaling policies**.

Policies: **target tracking**, such as 'keep average CPU at 50%', is the default choice; step scaling for finer control; scheduled scaling for known peaks; predictive scaling for regular patterns.

It doesn't make a single request faster; it adds capacity and replaces unhealthy instances. It only works cleanly for stateless services: sessions in Redis, files in S3, databases outside the group.

Details interviewers probe: **lifecycle hooks** to finish work or drain before termination; **scale-in protection** for an instance running a long job; cooldowns and warm-up to prevent flapping; and health checks from the load balancer, not just EC2 status."

Tham khảo thêm: [DevOps - EC2 Auto Scaling](https://minhnhat97kg.github.io/docsify/content/devops-ec2-auto-scaling/vi.md)

@@@ aws-eks | What do you need to know about running services on EKS? | devops | aws,eks,kubernetes | qa | AWS
"AWS runs the Kubernetes control plane; you manage the data plane: managed node groups, self-managed nodes, or Fargate.

Things that matter in practice:

- **Networking:** the VPC CNI gives each pod a real VPC IP, so pods can be targeted by security groups, but subnet IP space must be planned.
- **Pod permissions:** IRSA or EKS Pod Identity gives each service account its own IAM role. A pod reaches RDS through that role plus security groups, or with IAM database authentication.
- **Scaling:** HPA scales pods; Cluster Autoscaler or Karpenter adds nodes.
- **Security:** private API endpoint, secrets from Secrets Manager via the CSI driver, network policies.
- **Upgrades:** Kubernetes minor versions go out of standard support within about 14 months, so upgrades are routine: control plane first, then add-ons, then nodes, after checking for deprecated APIs."

Tham khảo thêm: [DevOps - Amazon EKS](https://minhnhat97kg.github.io/docsify/content/devops-amazon-eks-elastic-kubernetes-service/vi.md)

@@@ docker-go | How do you build a small, secure Docker image for a Go service? | devops | docker,go,devops | qa | Docker và Kubernetes
Multi-stage build: compile trong image có Go toolchain, chạy trong image tối giản.

```dockerfile
FROM golang:1.23 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -trimpath -ldflags="-s -w" -o /app ./cmd/api

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=build /app /app
USER nonroot
ENTRYPOINT ["/app"]
```

"Copying `go.mod` first caches the dependency layer. `CGO_ENABLED=0` produces a static binary that runs without libc. Distroless includes CA certificates and timezone data that `scratch` lacks, and runs as non-root. The result is usually 10–20 MB with almost no attack surface. `exec format error` means the binary was built for a different OS or CPU architecture; set `GOOS`/`GOARCH` or use `docker buildx` for multi-arch. Without a shell, I debug with `kubectl debug` and an ephemeral container."

Tham khảo thêm: [Docker Multistage Builds (Golang)](https://minhnhat97kg.github.io/docsify/content/devops-docker-multistage-builds-golang-optimization/vi.md)

@@@ k8s-debug | A pod is in CrashLoopBackOff. How do you debug it? | devops | kubernetes,troubleshooting,observability | qa | Docker và Kubernetes
"Step by step:

1. `kubectl describe pod` for events: OOMKilled, failed probes, image pull errors, missing ConfigMap or Secret.
2. `kubectl logs <pod> --previous` to see why the last container instance exited.
3. Check the exit code: 137 means killed, usually out of memory; 1 is an application error.
4. Common causes: wrong configuration or environment variables, the database unreachable at startup, a liveness probe that fires before the app is ready (use a startup probe), or memory limits too low.
5. If needed, `kubectl debug` with an ephemeral container, or run the image locally with the same configuration.

For observability, Prometheus **pulls** metrics by scraping `/metrics` endpoints and stores them as time series; logs go to Loki or ELK; traces to Jaeger or Tempo through OpenTelemetry. Kubernetes over Docker Swarm: much richer ecosystem, autoscaling and scheduling, at the cost of complexity."

Tham khảo thêm: [DevOps - Advance](https://minhnhat97kg.github.io/docsify/content/devops-advance/vi.md)

@@@ troubleshoot-10min | Production is slow and alerts are firing. Walk me through the first 10 minutes. | devops | troubleshooting,observability,incident | qa | Vận hành
"**Minutes 0–2, triage:** what's the user impact, which endpoints, since when? Check the dashboards for rate, errors and latency, and ask what changed: a deploy, a config change, a traffic spike, a dependency incident.

**Minutes 2–5, narrow down:** compare healthy and unhealthy instances or endpoints. Look at saturation: CPU, memory, GC pauses, thread or connection pools, database connections, queue lag.

**Minutes 5–8, trace:** pick slow traces and find the hop that dominates; check slow query logs and lock waits in the database.

**Minutes 8–10, mitigate before root-causing:** roll back the recent deploy, scale out, turn off the feature flag, or shed load with rate limits.

Throughout, I post short status updates in the incident channel. After recovery: root cause, then a blameless postmortem with actions such as an alert, a test or a runbook."

Tham khảo thêm: [Troubleshooting](https://minhnhat97kg.github.io/docsify/content/troubleshooting/vi.md)
